from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv('../.env')

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

key_points = """- AI is the capability of computational systems to perform tasks typically associated with human intelligence.
- These include learning, reasoning, problem-solving, perception, and decision-making.
- AI is multidisciplinary, spanning engineering, mathematics, and computer science."""

prompt = f"""Using only these key points, write a single encyclopedia-style paragraph about Artificial intelligence, in the style of a Wikipedia article, approximately 500 characters long. Do not add commentary or mention that you are an AI.

Key points:
{key_points}"""

msg = client.chat.completions.create(
    model='openai/gpt-oss-20b',
    max_tokens=1500,
    messages=[{'role': 'user', 'content': prompt}]
)

print('CONTENT:')
print(repr(msg.choices[0].message.content))
print()
print('FINISH REASON:', msg.choices[0].finish_reason)
print('REASONING TOKENS:', msg.usage.completion_tokens_details.reasoning_tokens)
print('TOTAL COMPLETION TOKENS:', msg.usage.completion_tokens)