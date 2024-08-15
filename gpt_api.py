import openai
import json
def get_api_key():
    openai_key_file = 'openai_key.json'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

openai.api_key = get_api_key()

ask = ""
completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a vtuber called open-source sama."},
        {
            "role": "user",
            "content": ask
        }
    ]
)

print(completion.choices[0].message)