import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from core import get_postgres_connection, get_milvus_client, get_embedding_model

def migrate_data():
    print("Initializing connections (Loading AI model may take a moment)...")
    pg_conn = get_postgres_connection()
    milvus_client = get_milvus_client()

    # If DBs aren't available, stop before loading the embedding model
    if not pg_conn or not milvus_client:
        print("Setup failed. Check your database connections in core.py.")
        return

    # Load the embedding model only after confirming DB connections
    model = get_embedding_model()

    # 1. Setup Milvus Collection
    collection_name = "medical_faq"
    vector_dimension = 384  # The E5-small-v2 model outputs exactly 384 dimensions
    
    if milvus_client.has_collection(collection_name=collection_name):
        print(f"Dropping old '{collection_name}' collection to start fresh...")
        milvus_client.drop_collection(collection_name=collection_name)
        
    print(f"Creating new '{collection_name}' collection in Milvus...")
    milvus_client.create_collection(
        collection_name=collection_name,
        dimension=vector_dimension,
        id_type="int",
        auto_id=False
    )

    # 2. Fetch Data from PostgreSQL
    cursor = pg_conn.cursor()
    try:
        cursor.execute("SELECT question, answer FROM medical")
        rows = cursor.fetchall()
        print(f"\nFound {len(rows)} medical records in PostgreSQL.")
        print("Starting AI vector translation (This will take a while)...")
    except Exception as e:
        print(f"Failed to read from PostgreSQL: {e}")
        return

    # 3. Translate and Insert in Batches
    batch_size = 100 # Processes 100 at a time to prevent RAM crashes
    data_to_insert = []
    
    for index, (question, answer) in enumerate(rows):
        # The E5 model requires the word "passage:" before documents it stores
        text_to_embed = f"passage: Q: {question} A: {answer}"
        vector = model.encode(text_to_embed).tolist()
        
        # Package the data for Milvus
        data_to_insert.append({
            "id": index + 1,  
            "vector": vector,
            "question": question,
            "answer": answer
        })
        
        # Push the batch to Milvus
        if len(data_to_insert) >= batch_size or index == len(rows) - 1:
            milvus_client.insert(collection_name=collection_name, data=data_to_insert)
            print(f"Inserted {index + 1} / {len(rows)} records into Milvus...")
            data_to_insert = [] 
            
    cursor.close()
    pg_conn.close()
    print("\nMIGRATION COMPLETE! Your Milvus vector database is fully loaded.")

if __name__ == "__main__":
    migrate_data()