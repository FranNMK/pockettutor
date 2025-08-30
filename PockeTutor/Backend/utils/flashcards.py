# backend/utils/flashcards.py
"""
Flashcard generation utility.
This connects to OpenAI (preferred) or Hugging Face to turn raw text into Q/A flashcards.
"""

import os
import openai

# Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_flashcards(text: str, n: int = 8):
    """
    Generate `n` study flashcards from the given text.
    Returns a list of dicts: {question: str, answer: str}
    """

    if not openai.api_key:
        return [{"question": "Error", "answer": "Missing OpenAI API key"}]

    prompt = (
        f"Create {n} educational flashcards from the text below.\n"
        f"Format each as 'Q: ...' and 'A: ...'.\n\n"
        f"Text:\n{text}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",   # lightweight + cheap
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )

        content = response["choices"][0]["message"]["content"]

        # Parse into flashcards
        cards = []
        q, a = None, None
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("Q:"):
                q = line[2:].strip()
            elif line.startswith("A:"):
                a = line[2:].strip()
                if q and a:
                    cards.append({"question": q, "answer": a})
                    q, a = None, None

        return cards if cards else [{"question": "No cards generated", "answer": content}]

    except Exception as e:
        return [{"question": "Error", "answer": str(e)}]
