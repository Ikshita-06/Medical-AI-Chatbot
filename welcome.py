# welcome.py
import re
from vocab import GREETINGS, GRATITUDE, UNSAFE_WORDS

def is_safe_input(query):
    query_lower = query.lower()
    if any(bad_word in query_lower for bad_word in UNSAFE_WORDS):
        return False, "I cannot fulfill this request. Please maintain respectful and safe language."
    return True, ""

def handle_small_talk(query):
    clean_q = re.sub(r'[^\w\s]', '', query.lower()).strip()
    words = clean_q.split()
    if not words: return None
    
    # If the exact phrase or the first word is a greeting
    if clean_q in GREETINGS or words[0] in GREETINGS:
        return "Hello! I am your Medical AI Assistant. How can I help you today?"
        
    if any(w in GRATITUDE for w in words) and len(words) <= 5:
        return "You're very welcome! Let me know if you need anything else."
        
    return None

def process_welcome(query):
    is_safe, msg = is_safe_input(query)
    if not is_safe:
        return True, msg 
        
    small_talk_reply = handle_small_talk(query)
    if small_talk_reply:
        return True, small_talk_reply 
        
    return False, None