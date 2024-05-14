import openai

class ChatHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def ask_chatgpt(self, question, context=""):
        messages = [
            {"role": "system", "content": (
                "You are a helpful assistant for RepoCrawler. Utilize the detailed metadata about the project to "
                "provide informed responses about the codebase, its usage, and documentation."
            )},
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                max_tokens=300,
                temperature=0.3,
                top_p=1.0,
                n=1
            )
            response_text = response.choices[0].message['content'].strip()
            token_count = response.usage['total_tokens']
            return response_text, token_count
        except Exception as e:
            return f"Failed to call ChatGPT API: {str(e)}", 0
