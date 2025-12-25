import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration (I chose not to use OpenAI because of payment issues)
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

# Local Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Data Configuration
DATA_PATH = "data/Restaurant Reviews.csv"
TEXT_COLUMN = "Review Text"

# ChromaDB Configuration
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "restaurant_reviews"

# Chunking Configuration
# Decision: NO CHUNKING - reviews are short (500-800 chars avg)
USE_CHUNKING = False

# Retrieval Configuration
TOP_K = 5  # Number of results to return
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score (0.5 is reasonable)