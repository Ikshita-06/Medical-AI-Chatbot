# core.py
import os
import psycopg2
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load hidden passwords from the .env file
load_dotenv()

def get_postgres_connection():
    """Connects to your PostgreSQL database where the text and memory live."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DBNAME", "postgres"), # Update this in your .env if your DB has a specific name
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
    """Connects to a lightweight, local Milvus file for vector storage."""
    try:
        # Milvus Lite creates this file automatically right inside your VS Code folder!
        client = MilvusClient("milvus_medical_demo.db")
        return client
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")
        return None

def get_embedding_model():
    """Loads the free, local E5 model to turn text into numbers."""
    print("Loading E5 model... (This might take a few seconds)")
    model = SentenceTransformer('intfloat/e5-small-v2')
    return model


# --- QUICK TEST TO SEE IF POSTGRES IS CONNECTED ---
if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    test_conn = get_postgres_connection()
    
    if test_conn:
        print("✅ SUCCESS! Your Python script is successfully talking to your database.")
        test_conn.close() # Always close the door behind you!
    else:
        print("❌ FAILED. Check your .env file passwords!")