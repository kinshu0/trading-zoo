import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

completion = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-70B-Instruct",
  messages=[
    {
        "role": "user",
        "content": """Hello!"""
    }
  ],
  temperature=0.6
)

print(completion.to_json())
    
