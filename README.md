# Medical Chatbot System: Semantic Search Architecture

## Overview

This repository contains the backend architecture for a Semantic Search Medical Chatbot. The system is designed to retrieve verified, medically accurate information from the MedQuad dataset. 

## System Architecture

The application logic is modularized into four primary components:

* **`welcome.py` (Ingress & Validation):** Serves as the initial entry point. It handles standard user greetings and implements strict guardrails to filter out non-medical queries before downstream processing.

* **`router.py` (Query Routing & FAQ Management):** The core decision engine. It evaluates incoming queries against a standard FAQ database for immediate resolution. For complex queries, it orchestrates context retrieval, vector search execution, and final response delivery.

* **`State.py` (Session State Management):** Manages short-term conversation context using a PostgreSQL backend. It implements a sliding-window algorithm to retain only the three most recent interactions.

* **`core.py` (Infrastructure Interfaces):** Contains the foundational utility functions. It manages database connection pooling for PostgreSQL, initializes the local Milvus Lite vector database, and loads the E5 text embedding model.

---

## Developer Onboarding Guide

Please follow these exact steps to configure your local development environment. Because the system relies on local databases and models, the code will not execute until this setup is complete.

### Step 1: Clone the Repository

Clone the project to your local machine and navigate into the root directory:

```bash
git clone https://github.com/Ikshita-06/Medical-AI-Chatbot.git
cd Medical-AI-Chatbot
```

### Step 2: Database Configuration

The system relies on PostgreSQL for text retrieval and session memory.

1. Ensure PostgreSQL and pgAdmin are installed locally.
2. Import the project's MedQuad dataset into your local PostgreSQL instance.
3. Open pgAdmin, connect to your database, and execute the following SQL to initialize the memory table:

```sql
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 3: Environment Configuration

Local database credentials are required but are excluded from version control for security purposes.

1. Locate the `.env.example` file in the project's root directory.
2. Copy the contents and create a new file named exactly `.env`.
3. Update the `PG_PASSWORD` and `PG_DBNAME` values in your new `.env` file to match your local pgAdmin configuration.

### Step 4: Install Dependencies

Initialize your Python environment and install the required packages. Note that specific versions of `setuptools` and `marshmallow` are enforced in the requirements file to ensure compatibility with the local Milvus client.

```bash
pip install -r requirements.txt
```

### Step 5: System Validation

To verify that the application successfully connects to your local database infrastructure, execute the core utility script:

```bash
python core.py
```

A successful execution will output a confirmation message indicating that the PostgreSQL connection is active. Once validated, you are ready to begin development.
