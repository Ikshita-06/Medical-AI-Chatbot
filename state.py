from core import get_postgres_connection

def save_message(message):
    """Saves a message to PostgreSQL and enforces the sliding window of 3."""
    conn = get_postgres_connection()
    if not conn:
        print("Could not connect to database to save memory.")
        return

    cursor = conn.cursor()
    try:
        # 1. Save the new message to the database
        cursor.execute("INSERT INTO chat_history (message) VALUES (%s)", (message,))
        
        # 2. THE SLIDING WINDOW: Keep only the 3 newest messages.
        delete_query = """
        DELETE FROM chat_history 
        WHERE id NOT IN (
            SELECT id FROM chat_history ORDER BY id DESC LIMIT 3
        )
        """
        cursor.execute(delete_query)
        
        conn.commit() 
    except Exception as e:
        print(f"Error saving to memory: {e}")
    finally:
        cursor.close()
        conn.close()

def get_current_memory():
    """Retrieves the recent chat history from PostgreSQL."""
    conn = get_postgres_connection()
    if not conn:
        return []
        
    cursor = conn.cursor()
    try:
        # Get the 3 most recent messages, ordered from oldest to newest so they read like a normal chat log
        cursor.execute("""
            SELECT message FROM (
                SELECT id, message FROM chat_history ORDER BY id DESC LIMIT 3
            ) AS recent_messages 
            ORDER BY id ASC
        """)
        
        rows = cursor.fetchall()
        
        # Pull just the text out of the database rows and put it in a standard Python list
        chat_list = [row[0] for row in rows]
        return chat_list
        
    except Exception as e:
        print(f"Error fetching memory: {e}")
        return []
    finally:
        cursor.close()
        conn.close()