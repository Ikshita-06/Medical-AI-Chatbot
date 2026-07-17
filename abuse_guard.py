import re
import time
from vocab import UNSAFE_WORDS

# Maximum abusive attempts
MAX_WARNINGS = 5

# Block duration (seconds)
BLOCK_TIME = 60

# Store warning count and block time
user_state = {
    "warnings": 0,
    "blocked_until": 0
}


def contains_abuse(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return any(word in UNSAFE_WORDS for word in words)


def check_abuse(message):

    current_time = time.time()

    # If user is blocked
    if current_time < user_state["blocked_until"]:

        remaining = int(user_state["blocked_until"] - current_time)

        return {
            "allowed": False,
            "blocked": True,
            "message": f"⛔ Chat terminated. Please wait {remaining} seconds.",
            "block_time": remaining
        }

    
    # If abusive word found
    if contains_abuse(message):

        user_state["warnings"] += 1

        remaining_warnings = MAX_WARNINGS - user_state["warnings"]

    # 5th warning -> Block chat
        if user_state["warnings"] >= MAX_WARNINGS:

            user_state["blocked_until"] = current_time + BLOCK_TIME
            user_state["warnings"] = 0

            return {
              "allowed": False,
              "blocked": True,
              "message": f"⛔ Chat terminated due to repeated abusive language.\nPlease wait {BLOCK_TIME} seconds.",
              "block_time": BLOCK_TIME
           }

    # 1st to 4th warning
        return  {
           "allowed": False,
           "blocked": False,
            "message": (
               f"⚠️ Please use appropriate language.\n"
               f"You have {remaining_warnings} warning(s) remaining.\n"
               f"After {remaining_warnings} more abusive message(s), "
               f"your chat will be terminated for {BLOCK_TIME} seconds."
            ),
            "block_time": 0
       }

    return {
        "allowed": True,
        "blocked": False,
        "message": "",
        "block_time": 0
    }