# Terms of Service Analyzer

## Overview
Automates analysis of Terms of Service agreements by identifying and explaining potential red flags in plain English.

## Core Features
- **Red Flag Detection:** Identifies clauses that may harm user rights.  
- **Severity Ranking:** Orders issues by potential impact.  
- **Plain-Language Explanations:** Translates legal jargon into clear, concise descriptions.  
- **Interactive Dashboard:** Presents findings in a React-based UI.

## Tech Stack
- **Frontend:** React  
- **Backend:** Flask (Python)  
- **Database:** Supabase (PostgreSQL)  
- **AI/LLM:** LLaMA-family models hosted via Groq  
- **Architecture:** Retrieval-Augmented Generation (RAG) pipeline

## Architecture (Brief)
1. **Ingestion:** Split document into sections, generate embeddings, store in Supabase.  
2. **Retrieval:** Fetch relevant sections by semantic similarity.  
3. **Analysis:** LLM processes retrieved context to detect and explain red flags.  
4. **Presentation:** API returns structured results to React UI.  
