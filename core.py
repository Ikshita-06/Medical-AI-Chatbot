import os
# Force the AI model to use the forgiving Python engine to avoid protobuf errors
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import psycopg2
from dotenv import load_dotenv

# Load environment variables (keeps your passwords safe)
load_dotenv()

def get_postgres_connection():
    """Connects to your PostgreSQL database where the text and memory live."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DBNAME", "Medical_data"), 
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "password"),
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def get_milvus_client():
    """
    Initializes and returns a connection to the local Milvus Lite vector database.
    """
    try:
        from pymilvus import MilvusClient
        # This is the magic line. It forces the router to look at the local file we built!
        client = MilvusClient(uri="./milvus_medical_demo.db")
        return client
    except Exception as e:
        print(f"Milvus client initialization error: {e}")
        return None

def get_embedding_model():
    """Loads the free, local E5 model to turn text into numbers."""
    print("Loading E5 model... (This might take a few seconds)")
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as e:
        print(f"Embedding model import error: {e}")
        return None

    try:
        model = SentenceTransformer('intfloat/e5-small-v2')
        return model
    except Exception as e:
        print(f"Failed to load embedding model: {e}")
        return None


# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    test_conn = get_postgres_connection()
    
    if test_conn:
        print("✅ SUCCESS! Connected to PostgreSQL database.")
        test_conn.close() 
    else:
        print("❌ FAILED to connect to PostgreSQL.")
        
    print("\nTesting Milvus connection...")
    test_milvus = get_milvus_client()
    
    if test_milvus:
        print("✅ SUCCESS! Connected to Milvus local database.")
    else:
        print("❌ FAILED to connect to Milvus.")