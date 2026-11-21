"""
=============================================================
    Smart Hire AI Agent
=============================================================
File Name: llm_engine.py
Author: Prajakta Shinde
Date:   14th Nov 2026

Description:
This file sends prompts to Groq's `openai/gpt-oss-120b`
model and receives intelligent evaluation responses.

Concepts Covered:
1. API Communication
2. LLM Integration
3. Prompt Transmission
4. Response Handling
5. Exception Handling
6. AI Agent Tool Calling

=============================================================
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Load .env from the project directory.
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)


def ask_groq(prompt):
    """
    Sends a prompt to Groq's `openai/gpt-oss-120b` model and
    returns the generated response.
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq API Error: {e}")
        raise
