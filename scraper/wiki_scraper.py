import wikipediaapi
import random
import json
import re
import time
import os

wiki = wikipediaapi.Wikipedia(user_agent="ai-slop-detector-research/1.0", language="en")

SEED_PAGES = [
    "Artificial intelligence", "History", "Biology", "Physics", "Music",
    "Geography", "Mathematics", "Literature", "Economics", "Philosophy"
]

def is_valid_title(title: str) -> bool:
    return ':' not in title

def is_valid_paragraph(text: str) -> bool:
    text = text.strip()
    if len(text) < 200 or len(text) > 1000:
        return False
    if re.match(r'^[\d\.\-\*]', text):
        return False
    if text.count('=') > 2:
        return False
    return True

def scrape_paragraphs(target_count=200):
    visited = set()
    to_visit = list(SEED_PAGES)
    paragraphs = []

    while to_visit and len(paragraphs) < target_count:
        title = to_visit.pop(0)
        if title in visited or not is_valid_title(title):
            continue
        visited.add(title)

        page = wiki.page(title)
        if not page.exists():
            continue

        candidates = [p for p in page.text.split('\n') if is_valid_paragraph(p)]
        for p in candidates[:2]:
            paragraphs.append({"title": title, "text": p.strip()})

        links = list(page.links.keys())
        random.shuffle(links)
        to_visit.extend(links[:3])

        print(f"[{len(paragraphs)}/{target_count}] scraped from: {title}")
        time.sleep(0.2)

    return paragraphs[:target_count]

if __name__ == "__main__":
    data = scrape_paragraphs(target_count=200)
    os.makedirs("../data", exist_ok=True)
    with open("../data/human_paragraphs.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} paragraphs to data/human_paragraphs.json")