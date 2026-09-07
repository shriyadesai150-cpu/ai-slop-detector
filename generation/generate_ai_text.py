import json
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from llm_client import call_llm

def summarize_key_points(paragraph: str) -> str:
    prompt = f"Extract the key factual points from this paragraph as a short bullet list. Only the facts, no commentary.\n\nParagraph:\n{paragraph}"
    return call_llm(prompt, max_tokens=800)

def rewrite_from_points(key_points: str, topic: str, target_length: int) -> str:
    approx_words = max(20, target_length // 6)  # rough chars-to-words estimate
    prompt = f"Using only these key points, write a single encyclopedia-style paragraph about {topic}, in the style of a Wikipedia article, roughly {approx_words} words long. Do not count characters precisely — just write naturally at approximately that length. Do not add commentary or mention that you are an AI.\n\nKey points:\n{key_points}"
    return call_llm(prompt, max_tokens=800)

def generate_ai_paragraph(human_paragraph: dict) -> dict:
    key_points = summarize_key_points(human_paragraph["text"])
    target_length = len(human_paragraph["text"])
    ai_text = rewrite_from_points(key_points, human_paragraph["title"], target_length)
    if not ai_text or not ai_text.strip():
        raise ValueError(f"Empty AI text generated for: {human_paragraph['title']}")
    return {
        "title": human_paragraph["title"],
        "text": ai_text.strip()
    }

if __name__ == "__main__":
    with open("../data/human_paragraphs.json") as f:
        human_data = json.load(f)[:5]  # TEST: only first 5

    ai_data = []
    for i, item in enumerate(human_data, 1):
        try:
            ai_item = generate_ai_paragraph(item)
            ai_data.append(ai_item)
            print(f"[{i}/{len(human_data)}] generated AI version for: {item['title']}")
        except Exception as e:
            print(f"[{i}/{len(human_data)}] FAILED for {item['title']}: {e}")

    with open("../data/ai_paragraphs.json", "w") as f:
        json.dump(ai_data, f, indent=2)

    print(f"\nSaved {len(ai_data)} AI-generated paragraphs to data/ai_paragraphs.json")