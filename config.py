import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_openai_api_key")

# --- File Paths ---
# Defines the paths for data storage and uploads.
UPLOAD_FOLDER = 'static/uploads'
CANDIDATES_FILE = 'data/candidates.json'
ASSESSMENTS_FILE = 'data/assessments.json'
RESPONSES_FILE = 'data/responses.json'
FAISS_INDEX_PATH = 'faiss_index/skill_assessment.index'

# --- Assessment Configuration ---
# The model used for generating assessment questions.
ASSESSMENT_MODEL = "gpt-4"
# The model used for generating embeddings for scoring.
EMBEDDING_MODEL = "text-embedding-ada-002"

# --- Application Configuration ---
# Secret key for Flask session management.
SECRET_KEY = os.urandom(24)
