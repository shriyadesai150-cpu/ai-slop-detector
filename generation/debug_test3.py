import json
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv('../.env')

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

key_points = """- AI is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making.
- AI is a field of research in engineering, mathematics, and computer science.
- The field develops and studies methods and software that enable machines to perceive their environment.
- Machines use learning and intelligence to take actions that maximize their chances of achieving defined goals."""

target_length = 493
prompt = f"Using only these key points, write a single encyclopedia-style paragraph about Artificial intelligence, in the style of a Wikipedia article, approximately {target_length} characters long. Do not add commentary or mention that you are an AI.\n\nKey points:\n{key_points}"

msg = client.chat.completions.create(
    model='openai/gpt-oss-20b',
    max_tokens=1500,
    messages=[{'role': 'user', 'content': prompt}]
)

print('CONTENT:', repr(msg.choices[0].message.content))
print('FINISH REASON:', msg.choices[0].finish_reason)
print('REASONING TOKENS:', msg.usage.completion_tokens_details.reasoning_tokens)
print('TOTAL COMPLETION TOKENS:', msg.usage.completion_tokens)
print()
print('REASONING TEXT:')
print(msg.choices[0].message.reasoning)