import os
import re
from textblob import TextBlob
# Force the AI model to use the forgiving Python engine to avoid protobuf errors
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from core import get_postgres_connection, get_milvus_client, get_embedding_model
from welcome import is_safe_input
from state import save_message, get_current_memory

COLLECTION_NAME = "medical_faq"

# 🚀 Load the AI Brain ONCE at startup so the chat loop is lightning fast
print("Initializing AI Brain... (Please wait)")
milvus_client = get_milvus_client()
model = get_embedding_model()

if milvus_client:
    # Wake up the database so it doesn't crash on search
    milvus_client.load_collection(collection_name=COLLECTION_NAME)

def clean_and_summarize(raw_text, max_sentences=3):
    """Cleans out scraped junk and cuts the text down to a brief summary."""
    if not raw_text:
        return raw_text
        
    clean_text = re.sub(r'\(.*?video.*?\)', '', raw_text, flags=re.IGNORECASE)
    clean_text = clean_text.replace("Key Points", "")
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    sentences = re.split(r'(?<=[.!?]) +', clean_text)
    short_answer = " ".join(sentences[:max_sentences])
    
    return short_answer.strip()

def resolve_context(current_query):
    """
    🧠 THE SLIDING MEMORY DETECTIVE
    Tracks the main topic across multiple follow-ups using the Postgres history.
    """
    history = get_current_memory()
    if not history:
        return current_query
        
    current_lower = current_query.lower()
    words = current_lower.split()
    
    follow_up_keywords = [
        "cause", "causes", "symptom", "symptoms", "treat", "treatment", 
        "precaution", "precautions", "prevent", "prevention", "cure", 
        "medicine", "medication", "risk", "risks"
    ]
    
    is_follow_up = False
    if " it" in current_lower or " this" in current_lower or current_lower in ["it", "this"]:
        is_follow_up = True
    elif len(words) <= 4 and any(k in words for k in follow_up_keywords):
        is_follow_up = True
        
    if not is_follow_up:
        return current_query
        
    # Dig backward through the Postgres memory to find the Anchor Topic
    anchor = ""
    for chat in reversed(history):
        if " | Bot: " not in chat: continue
        
        past_user_q = chat.split(" | Bot: ")[0].replace("User: ", "").strip()
        past_lower = past_user_q.lower()
        past_words = past_lower.split()
        
        past_is_follow_up = False
        if " it" in past_lower or " this" in past_lower or past_lower in ["it", "this"]:
            past_is_follow_up = True
        elif len(past_words) <= 4 and any(k in past_words for k in follow_up_keywords):
            past_is_follow_up = True
            
        if not past_is_follow_up:
            anchor = past_user_q
            break
            
    if anchor:
        print(f"   [DEBUG] 🧠 Sliding Memory: Linked '{anchor}' to '{current_query}'")
        return f"{anchor} {current_query}"
        
    return current_query

def search_postgres(query):
    """First check whether the question exists exactly in PostgreSQL."""
    conn = get_postgres_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT answer FROM medical WHERE LOWER(question)=LOWER(%s) LIMIT 1",
            (query,),
        )
        row = cursor.fetchone()
        if row: return row[0]
        return None
    except Exception as e:
        return None
    finally:
        cursor.close()
        conn.close()

def search_milvus(query):
    """Semantic Search using E5 embeddings + Milvus"""
    if not milvus_client or not model:
        return "Milvus connection failed."

    text_to_embed = f"query: {query}"
    
    try:
        query_embedding = model.encode(text_to_embed).tolist()
        
        results = milvus_client.search(
            collection_name=COLLECTION_NAME,
            data=[query_embedding],
            limit=1,
            output_fields=["question", "answer"],
        )

        if results and len(results[0]) > 0:
            hit = results[0][0]
            distance = hit.get("distance", 0)
            
            # 🛡️ THE BOUNCER: Loosened to 0.18 to allow for longer "memory stitched" questions
            if distance > 0.18:
                return "I couldn't find a confident match for that. Please check for typos and try asking again."
            
            return hit["entity"]["answer"]

        return "Sorry, I could not find any relevant medical information."

    except Exception as e:
        return "Error searching medical database."

def process_query(user_query):
    """Main Router"""
    
    # 1. 🚀 THE SPELLCHECK FIX: Strip punctuation first so TextBlob doesn't crash
    clean_for_spell = re.sub(r'[^\w\s]', '', user_query)
    corrected_query = str(TextBlob(clean_for_spell).correct())
    
    if corrected_query.lower() != clean_for_spell.lower():
        print(f"   [DEBUG] Autocorrected to: '{corrected_query}'")

    # 2. 🧠 Memory Context Intercept (Adds Anchor to follow-ups)
    smart_query = resolve_context(corrected_query)

    # 3. Bouncer Check (Is it safe?)
    valid, message = is_safe_input(smart_query)
    if not valid:
        return message

    # 4. Search Postgres
    raw_answer = search_postgres(smart_query)

    # 5. Search AI Database
    if not raw_answer:
        raw_answer = search_milvus(smart_query)

    # 6. Clean up the paragraphs AND handle memory saving safely
    if "confident match" not in raw_answer and "Sorry" not in raw_answer and "Error" not in raw_answer:
        final_answer = clean_and_summarize(raw_answer)
        
        # 💾 THE MEMORY FIX: Only save successful medical answers to the Postgres database!
        memory_string = f"User: {corrected_query} | Bot: {final_answer}"
        save_message(memory_string)
    else:
        # If it's an error message, output it but DO NOT save it to history.
        final_answer = raw_answer

    return final_answer

if __name__ == "__main__":
    print("\n✅ Medical Chatbot Started! Type 'exit' to quit.\n")
    
    while True:
        query = input("You : ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        response = process_query(query)
        print(f"\nBot : {response}\n")
        