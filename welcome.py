def get_welcome_message():
    """
    Returns the standardized greeting and capability disclaimer for the assistant.
    """
    return (
        "Hello. I am your Semantic Medical Assistant. "
        "I provide information using verified, doctor-approved data "
        "from the MedQuad database. Please enter your medical query."
    )

def is_safe_input(user_input):
    """
    Validates user input against predefined guardrails to ensure relevance and system security.
    Returns a tuple containing a boolean validation flag and the corresponding status message.
    """
    if not user_input or not isinstance(user_input, str):
        return False, "Input error: Please provide a valid text query."
        
    text = user_input.strip().lower()
    
    if not text:
        return False, "Input error: Query cannot be empty."
        
    # Detect anomalous input (e.g., uninterrupted character strings)
    if len(text) > 15 and " " not in text:
        return False, "Input error: Query format is unrecognizable. Please use standard phrasing."
        
    # Enforce domain-specific constraints
    blocked_keywords = [
        "poem", "recipe", "code", "weather", "joke", 
        "story", "essay", "ignore all previous", "translate"
    ]
    
    if any(word in text for word in blocked_keywords):
        return False, "Out of scope: This system is strictly configured for medical data retrieval."
        
    return True, "Valid"