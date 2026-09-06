import os
import time
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq")
MAX_RETRIES = 3

def call_llm(prompt: str, max_tokens: int = 500) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            if PROVIDER == "groq":
                from groq import Groq
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                msg = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return msg.choices[0].message.content

            elif PROVIDER == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                msg = client.chat.completions.create(
                    model="gpt-5-nano",
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return msg.choices[0].message.content

            else:
                raise ValueError(f"Unknown LLM_PROVIDER: {PROVIDER}")

        except Exception as e:
            wait = 2 ** attempt
            print(f"[call_llm] attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(wait)