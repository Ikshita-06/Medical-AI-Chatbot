# ==========================================
# 1. THE FOLLOW-UP TRIGGERS
# ==========================================
# If a user types ANY of these words, the bot knows they are asking a follow-up 
# about the previously mentioned disease, rather than bringing up a new one.
FOLLOW_UP_KEYWORDS = {
    "cause", "causes", "symptom", "symptoms", "treat", "treatment", "treatments",
    "identify", "identifications", "precaution", "precautions", "prevent", "prevention",
    "genetic", "cure", "cures", "medicine", "medicines", "medication", "medications",
    "risk", "risks", "diagnose", "diagnosis", "test", "tests", "testing",
    "manage", "management", "therapy", "surgery", "signs", "indicators", 
    "remedy", "remedies", "pills", "drugs", "side effects", "complications", 
    "stages", "types", "vaccine", "vaccines", "diet", "food", "check", "screening",
    "recover", "recovery", "relief", "heal", "healing", "hereditary", "spread", "contagious","details",
    "detail","overview","explain","explanation","more","more info","information","tell more","describe","severity",
    "serious","prognosis","outlook","survival","life expectancy","duration","long term","short term","complication","complications"
}


# ==========================================
# 2. THE INTENT NORMALIZER (The Translation Brain)
# ==========================================
# Maps chaotic human slang and variations to standard medical terms your database understands.
INTENT_SYNONYMS = {
    "symptoms": [
        "how to identify", "signs", "how to tell", "what does it look like", 
        "identifications", "how to know if", "how to detect", "warning signs", 
        "red flags", "indicators", "how to spot", "what are the signs", 
        "feeling sick with", "symptoms of", "clinical features", "what happens when",
        "do i have", "how do i know", "am i showing signs", "what to look for", 
        "physical signs", "early signs", "how it presents", "presentation",
        "how does it feel", "what are the indicators", "clues"
    ],
    
    "causes": [
        "why does it happen", "reason for", "what brings it on", "how do you get", 
        "what triggers", "origin of", "source of", "what causes", "how is it caused", 
        "main cause", "root cause", "where does it come from", "why do i have",
        "how did i get", "etiology", "provoked by", "started by", "leads to", 
        "resulting from", "reason behind", "why do people get"
    ],
    
    "treatment": [
        "how to cure", "how to fix", "remedy", "what can i take", "how to manage", 
        "therapy", "medication for", "medicine for", "how to treat", "treatment options", 
        "best treatment", "heal", "relief for", "how to get rid of", "surgery for", 
        "is there a cure", "can it be cured", "pills for", "drugs for", "how to recover", 
        "rehabilitation", "intervention", "treatment plan", "prescriptions", 
        "how to survive", "what to do if i have", "fixing", "curing"
    ],
    
    "precaution": [
        "how to prevent", "safety", "avoid", "prevention", "how to avoid", 
        "protect against", "reduce risk", "precautions for", "preventative", 
        "stop it from happening", "stay safe from", "lifestyle changes", 
        "preventive measures", "prophylaxis", "ward off", "how not to get", 
        "steps to avoid", "keep away from"
    ],
    
    "diagnosis": [
        "how to test", "test for", "check for", "how is it diagnosed", "medical tests", 
        "screening", "mri", "blood test", "how to check", "biopsy", "testing for", 
        "diagnosing", "lab test", "imaging", "x-ray", "ultrasound", "scan", "exam", 
        "evaluation", "how to confirm", "finding out if i have"
    ],
    
    "risk_factors": [
        "am i at risk", "who gets this", "chances of getting", "likelihood", 
        "is it hereditary", "is it genetic", "runs in the family", "risk factors", 
        "is it contagious", "can it spread", "susceptibility", "predisposition", 
        "vulnerable to", "who is affected", "can i catch it", "is it infectious"
    ],
    
    "what is": [
        "define", "meaning of", "explain", "what does it mean", "overview of", 
        "summary of", "describe", "what exactly is", "can you explain", "tell me about",
        "what is","what are","what's","whats"
    ]
}


# ==========================================
# 3. STOP WORDS (The Noise Filter)
# ==========================================
# Common conversational filler words we strip out before searching Milvus. 
# This forces the AI to focus STRICTLY on the heavy medical terms.
STOP_WORDS = {
    # Question words & Articles
    "what", "is", "the", "a", "an", "how", "to", "do", "i", "have", "of", "for", 
    "can", "it", "are", "does", "did", "will", "would", "should", "could", "which",
    "who", "whom", "whose", "where", "when", "why",
    
    # Pronouns & Prepositions
    "my", "your", "his", "her", "their", "our", "we", "they", "he", "she", 
    "me", "us", "them", "this", "that", "these", "those", "in", "on", "at", 
    "by", "with", "from", "as", "into", "through", "during", "before", "after",
    
    # Verbs & Conversational Fillers
    "am", "was", "were", "be", "been", "being", "has", "had", "doing", 
    "tell", "show", "give", "know", "about", "like", "just", "please", 
    "kindly", "help", "info", "information", "meant", "mean", "get", "got", 
    "getting", "make", "made", "making", "think", "thought", "see", "saw", "look",
    "any", "some", "all", "every", "each", "one", "two", "three", "first", "second",
    "pls","plz","please"
}


# ==========================================
# 4. SMALL TALK & GREETINGS
# ==========================================
GREETINGS = {
    "hi", "hello", "hey", "hii", "heyo", "greetings", "good morning", 
    "good afternoon", "good evening", "sup", "yo", "namaste", "hiya", "howdy",
    "hi there", "hello there", "heyy", "hallo", "hola"
}

GRATITUDE = {
    "thanks", "thank you", "thx", "tysm", "thanks a lot", "appreciate it", 
    "thankyou", "awesome", "great", "helpful", "good job", "cheers", 
    "perfect", "much appreciated", "thanks bro", "thank u", "ty", "you rock",
    "thanks so much", "very helpful","ok", "okay", "alright", "got it", "understood",
    "makes sense", "cool", "fine"
}

UNSAFE_WORDS = {
    "abuse", "stupid", "idiot", "fake", "dumb", "useless", 
    "hate", "shut up", "fuck", "shit", "bitch", "asshole"
}