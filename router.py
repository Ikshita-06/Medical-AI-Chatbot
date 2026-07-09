from state import save_message
from welcome import process_welcome
from faq import process_faq

def process_query(user_query):
    """The Main Orchestrator (Bridge)"""
    
    # 1. Welcome Agent (Filters greetings & abuse instantly)
    is_handled, welcome_response = process_welcome(user_query)
    if is_handled:
        save_message(f"User: {user_query} | Bot: {welcome_response}")
        return welcome_response
        
    # 2. FAQ Agent (The heavy lifter that handles medical math)
    corrected_query, faq_response = process_faq(user_query)
    save_message(f"User: {corrected_query} | Bot: {faq_response}")
    return faq_response

if __name__ == "__main__":
    print("\n✅ Medical Chatbot Started! Type 'exit' to quit.\n")
    print("Bot : Hello! I am your Medical AI Assistant. How can I help you today?\n")
    
    while True:
        query = input("You : ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        response = process_query(query)
        print(f"\nBot : {response}\n")