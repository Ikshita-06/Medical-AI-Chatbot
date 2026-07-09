# In-memory storage for sliding window history and strict medical topic tracking.

_chat_history = []
_current_topic = None

def get_current_topic():
    """Returns the isolated, currently active medical topic (e.g., 'lung cancer')."""
    return _current_topic

def set_current_topic(topic):
    """Sets the isolated medical topic when a new disease is detected."""
    global _current_topic
    _current_topic = topic

def get_current_memory():
    """Returns the sliding window chat history."""
    return _chat_history

def save_message(message_string):
    """Saves a formatted conversation string and maintains a rolling window of 3."""
    global _chat_history
    _chat_history.append(message_string)
    
    # Enforce Sliding Window (Last 3 interactions)
    if len(_chat_history) > 3:
        _chat_history.pop(0)

def clear_memory():
    """Wipes the session memory and topic state."""
    global _chat_history, _current_topic
    _chat_history = []
    _current_topic = None