import json

with open("human_paragraphs.json") as f:
    human = json.load(f)[:40]  # match the subset used for generation

with open("ai_paragraphs.json") as f:
    ai = json.load(f)

labeled = []
for item in human:
    labeled.append({"text": item["text"], "label": 0, "title": item["title"]})  # 0 = human
for item in ai:
    labeled.append({"text": item["text"], "label": 1, "title": item["title"]})  # 1 = AI

with open("labeled_dataset.json", "w") as f:
    json.dump(labeled, f, indent=2)

print(f"Saved {len(labeled)} labeled examples ({len(human)} human, {len(ai)} AI) to labeled_dataset.json")