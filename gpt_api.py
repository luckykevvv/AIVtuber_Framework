import openai
import json

def get_api_key():
    openai_key_file = 'openai_key.json'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

openai.api_key = get_api_key()

# Initialize the conversation with the vtuber role
message_init = [{"role": "system", "content": "You are a vtuber called open-source sama."}]
messages = message_init

def ask_gpt(messages):
    rsp = openai.chat.completions.create(
        model="gpt-4o-mini",  # Ensure this is the correct model identifier
        messages=messages
    )
    return rsp.choices[0].message.content

while True:
    # Limit the conversation history
    if len(messages) >= 5:
        print("******************************")
        print("*****maximum conversation*****")
        print("******************************")
        messages = messages[-4:]  # Keep only the last 10 messages

    # Ask the user for input
    ask = input('Ask: ')
    
    # Append the user's question and get the response
    messages.append({"role": "user", "content": ask})
    print(messages)
    answer = ask_gpt(messages)
    print(f"【ChatGPT】{answer}")
    messages.append({"role": "assistant", "content": answer})
