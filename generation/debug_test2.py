import json
from llm_client import call_llm

with open("../data/human_paragraphs.json") as f:
    human_data = json.load(f)

item = human_data[0]  # first real paragraph
print(f"Testing with: {item['title']}, length: {len(item['text'])}")

prompt1 = f"Extract the key factual points from this paragraph as a short bullet list. Only the facts, no commentary.\n\nParagraph:\n{item['text']}"
key_points = call_llm(prompt1, max_tokens=800)
print("\nKEY POINTS:")
print(key_points)

target_length = len(item['text'])
prompt2 = f"Using only these key points, write a single encyclopedia-style paragraph about {item['title']}, in the style of a Wikipedia article, approximately {target_length} characters long. Do not add commentary or mention that you are an AI.\n\nKey points:\n{key_points}"
ai_text = call_llm(prompt2, max_tokens=1500)
print("\nAI TEXT:")
print(repr(ai_text))