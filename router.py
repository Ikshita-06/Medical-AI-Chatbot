# router.py
from state import save_message
from welcome import process_welcome
from faq import process_faq
from abuse_guard import check_abuse

def process_query(user_query):
    """Main Orchestrator"""

    # Step 1: Check for abusive language
    abuse_result = check_abuse(user_query)

    if not abuse_result["allowed"]:
        return abuse_result["message"]

    # Step 2: Welcome Agent
    is_handled, welcome_response = process_welcome(user_query)

    if is_handled:
        save_message(f"User: {user_query} | Bot: {welcome_response}")
        return welcome_response

    # Step 3: FAQ Agent
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