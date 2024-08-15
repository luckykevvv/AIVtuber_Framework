import openai
import json

def get_api_key():
    openai_key_file = 'openai_key.json'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

openai.api_key = get_api_key()

class ChatGPT():
    def __init__(self) -> None:
        self.message_init = [{"role": "system", "content": "You are a vtuber called open-source sama."}]
        self.messages = self.message_init

    def ask_gpt(self):
        rsp = openai.chat.completions.create(
            model="gpt-4o-mini",  # Ensure this is the correct model identifier
            messages=self.messages
        )
        return rsp.choices[0].message.content

    def asking(self, question):
        if len(self.messages) >= 11:
            print("******************************")
            print("*****maximum conversation*****")
            print("******************************")
            self.messages=self.message_init

        ask = question
        self.messages.append({"role": "user", "content": ask})
        
        answer = self.ask_gpt()
        self.messages.append({"role": "assistant", "content": answer})
        return answer
