from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

def get_llm_response(prompt: str, system_prompt: str = "", model: str = DEFAULT_MODEL) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
