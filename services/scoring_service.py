import numpy as np
import faiss
from services.openai_service import get_embedding
from config import FAISS_INDEX_PATH
import os

def score_response(response_text, model_answer):

    # Get the vector embeddings for both the candidate's answer and the model answer
    response_embedding = get_embedding(response_text)
    model_embedding = get_embedding(model_answer)

    # If either embedding could not be generated, return a score of 0
    if not response_embedding or not model_embedding:
        return 0.0

    # Convert lists to numpy arrays for calculation
    response_vec = np.array([response_embedding]).astype('float32')
    model_vec = np.array([model_embedding]).astype('float32')
    
    # Normalize the vectors to unit vectors
    faiss.normalize_L2(response_vec)
    faiss.normalize_L2(model_vec)
    
    # Calculate the dot product (cosine similarity) between the two vectors
    # The result will be between -1 and 1.
    similarity = np.dot(response_vec[0], model_vec[0])
    
    # Convert the similarity score to a percentage (0-100 scale)
    # We scale from [-1, 1] to [0, 100]
    score = (similarity + 1) / 2 * 100
    
    return round(score, 2)

def create_and_search_faiss_index(model_answers, candidate_answer):
   
    model_embeddings = [get_embedding(ans) for ans in model_answers if get_embedding(ans)]
    candidate_embedding = get_embedding(candidate_answer)

    if not model_embeddings or not candidate_embedding:
        return None, None

    embeddings_np = np.array(model_embeddings).astype('float32')
    dimension = embeddings_np.shape[1]
    
    # Using IndexFlatIP for cosine similarity after normalization
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings_np)
    index.add(embeddings_np)

    candidate_vec = np.array([candidate_embedding]).astype('float32')
    faiss.normalize_L2(candidate_vec)

    # Search the index for the top 1 closest match
    k = 1
    distances, indices = index.search(candidate_vec, k)
    
    return distances, indices
