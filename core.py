import os
import psycopg2
from dotenv import load_dotenv

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
    # Lazy import to avoid importing pymilvus at module import time
    try:
        from pymilvus import MilvusClient
    except Exception as e:
        print(f"Milvus client import error: {e}")
        return None

    # Try several common local URIs used by Milvus / milvus-lite installations.
    candidate_uris = [
        "http://127.0.0.1:19121",
        "http://localhost:19121",
        "http://127.0.0.1:19530",
        "http://localhost:19530",
    ]

    last_exc = None
    for uri in candidate_uris:
        try:
            client = MilvusClient(uri=uri)
            return client
        except Exception as e:
            last_exc = e

    # Try without an explicit URI (allow env/config to take effect)
    try:
        client = MilvusClient()
        return client
    except Exception as e:
        last_exc = e

    print(f"Milvus client initialization error: {last_exc}")
    print("Hint: ensure Milvus or milvus-lite is running and reachable at localhost.\n"
          "If using milvus-lite, install the extra with: pip install 'pymilvus[milvus_lite]'\n"
          "and start the milvus-lite service before running this script.")
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


# --- QUICK TEST TO SEE IF POSTGRES IS CONNECTED ---
if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    test_conn = get_postgres_connection()
    
    if test_conn:
        print("SUCCESS! Python script is successfully connected to database.")
        test_conn.close() 
    else:
        print("FAILED.")