import os
import re
from textblob import TextBlob
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from core import get_postgres_connection, get_milvus_client, get_embedding_model
from state import get_current_memory

from vocab import INTENT_SYNONYMS, FOLLOW_UP_KEYWORDS, STOP_WORDS

COLLECTION_NAME = "medical_faq"

print("Initializing FAQ Agent Brain... (Please wait)")
milvus_client = get_milvus_client()
model = get_embedding_model()

if milvus_client:
    milvus_client.load_collection(collection_name=COLLECTION_NAME)

def clean_and_summarize(raw_text, max_sentences=3):
    if not raw_text: return raw_text
    clean_text = re.sub(r'\(.*?video.*?\)', '', raw_text, flags=re.IGNORECASE)
    clean_text = clean_text.replace("Key Points", "")
    clean_text = re.sub(r'button on your keyboard.*?\)', '', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    sentences = re.split(r'(?<=[.!?]) +', clean_text)
    return " ".join(sentences[:max_sentences]).strip()

def normalize_vocabulary(query):
    query_lower = query.lower()
    for standard_term, synonyms in INTENT_SYNONYMS.items():
        if any(syn in query_lower for syn in synonyms):
            return standard_term
    return query

def resolve_context(current_query):
    """🧠 THE SLIDING MEMORY DETECTIVE"""
    history = get_current_memory()
    
    clean_current = re.sub(r'[^\w\s]', '', current_query.lower()).strip()
    words = clean_current.split()
    
    core_words = [w for w in words if w not in STOP_WORDS]
    
    is_follow_up = False
    if " it" in clean_current or " this" in clean_current or clean_current in ["it", "this"]:
        is_follow_up = True
    elif len(core_words) > 0 and all(w in FOLLOW_UP_KEYWORDS for w in core_words):
        is_follow_up = True
        
    if not is_follow_up:
        if len(core_words) <= 2 and "what" not in clean_current:
            return f"what is {current_query}"
        return current_query
        
    if not history:
        return current_query
        
    anchor = ""
    for chat in reversed(history):
        if " | Bot: " not in chat: continue
        
        past_user_q = chat.split(" | Bot: ")[0].replace("User: ", "").strip()
        clean_past = re.sub(r'[^\w\s]', '', past_user_q.lower()).strip()
        past_words = clean_past.split()
        
        past_core_words = [w for w in past_words if w not in STOP_WORDS]
        
        past_is_follow_up = False
        if " it" in clean_past or " this" in clean_past or clean_past in ["it", "this"]:
            past_is_follow_up = True
        elif len(past_core_words) > 0 and all(w in FOLLOW_UP_KEYWORDS for w in past_core_words):
            past_is_follow_up = True
            
        if not past_is_follow_up:
            anchor = past_user_q
            break
            
    if anchor:
        prefixes = r'^(can you tell me about|can u tell me about|can u brief me about|brief me about|what do you know about|tell me about|what is|what are|explain|describe|define|is|can|do|does)\s+'
        clean_anchor = re.sub(prefixes, '', anchor.lower()).strip()
        clean_anchor = re.sub(r'[^\w\s]', '', clean_anchor).strip()
        
        clean_intent = normalize_vocabulary(current_query)
        clean_intent = re.sub(r'[^\w\s]', '', clean_intent).strip()
        
        final_query = f"{clean_intent} of {clean_anchor}"
        print(f"   [DEBUG] 🧠 Formatted Search Query: '{final_query}'")
        return final_query
        
    return current_query

def search_postgres(query):
    conn = get_postgres_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT answer FROM medical WHERE LOWER(question)=LOWER(%s) LIMIT 1", (query,))
        row = cursor.fetchone()
        if row: return row[0]
        
        cursor.execute("SELECT answer FROM medical WHERE question ILIKE %s LIMIT 1", (f"{query}%",))
        row = cursor.fetchone()
        return row[0] if row else None
    except: return None
    finally:
        cursor.close()
        conn.close()

def search_milvus(query):
    if not milvus_client or not model: return "Milvus connection failed."
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
            
            if distance > 0.25:
                return "I couldn't find a confident match for that. Please check for typos and try asking again."
            return hit["entity"]["answer"]
        return "Sorry, I could not find any relevant medical information."
    except: return "Error searching medical database."

def process_faq(user_query):
    clean_for_spell = re.sub(r'[^\w\s\?]', '', user_query)
    corrected_query = str(TextBlob(clean_for_spell).correct())

    normalized_query = normalize_vocabulary(corrected_query)
    smart_query = resolve_context(normalized_query)

    raw_answer = search_postgres(smart_query)
    if not raw_answer:
        raw_answer = search_milvus(smart_query)

    error_flags = ["confident match", "Sorry", "Error searching", "Milvus connection failed"]
    if not any(flag in raw_answer for flag in error_flags):
        final_answer = clean_and_summarize(raw_answer)
        return corrected_query, final_answer
    else:
        return corrected_query, raw_answer