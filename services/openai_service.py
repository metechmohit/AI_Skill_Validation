from openai import OpenAI
from config import OPENAI_API_KEY, ASSESSMENT_MODEL, EMBEDDING_MODEL

# Initialize the OpenAI client with your API key
# This is the new syntax for openai v1.0.0+
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_text(prompt):
    """
    Generates text using the specified OpenAI Chat model with the new client syntax.

    Args:
        prompt (str): The prompt to send to the model.

    Returns:
        str: The generated text from the model, or None if an error occurs.
    """
    try:
        # The method call is now client.chat.completions.create
        response = client.chat.completions.create(
            model=ASSESSMENT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        # The way to access the response content has also changed
        return response.choices[0].message.content.strip()
    except Exception as e:
        # The error message from the traceback will be printed here
        print(f"An error occurred in generate_text: {e}")
        return None

def get_embedding(text):
    """
    Generates a vector embedding for a given text using the new client syntax.

    Args:
        text (str): The input text to embed.

    Returns:
        list: A list of floats representing the embedding vector, or None if an error occurs.
    """
    try:
        # Sanitize input text by replacing newlines
        text = text.replace("\n", " ")
        # The method call is now client.embeddings.create
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        # Accessing the data is also slightly different
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred in get_embedding: {e}")
        return None
