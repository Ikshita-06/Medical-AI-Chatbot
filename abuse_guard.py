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

        if user_state["warnings"] >= MAX_WARNINGS:

            print("\n⛔ Chat terminated because of repeated abusive language.\n")

            # Reset warnings
            user_state["warnings"] = 0

            # Live countdown
            for remaining in range(BLOCK_TIME, 0, -1):
                print(f"\r⏳ Wait for {remaining} seconds...", end="", flush=True)
                time.sleep(1)

            print("\n\n✅ Chat started again.\n")

        return {
            "allowed": False,
            "blocked": False,
            "message": f"⚠️ Please use appropriate language.\nOnly {remaining_warnings} warning(s) remaining.",
            "block_time": 0
        }

        return {
            "allowed": False,
            "blocked": False,
            "message": f"⚠ Please use appropriate language.\nOnly {remaining_warnings} warning(s) remaining.",
            "block_time": 0
        }

    return {
        "allowed": True,
        "blocked": False,
        "message": "",
        "block_time": 0
    }