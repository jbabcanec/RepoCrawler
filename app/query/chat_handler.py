# app/query/chat_handler.py
import openai

class ChatHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def ask_chatgpt(self, question, context=""):
        role_description = (
            "As a helpful assistant for RepoCrawler, utilize the detailed metadata about the project to "
            "provide informed responses about the codebase, its usage, and documentation. Below is the project context:\n"
        )
        full_prompt = f"{role_description}{context}\nQuestion: {question}\nAnswer:"
        #print(full_prompt)
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=full_prompt,
                max_tokens=300,
                temperature=0.3,
                top_p=1.0,
                n=1,
                stop=None,
                api_key=self.api_key
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Failed to call ChatGPT API: {str(e)}"