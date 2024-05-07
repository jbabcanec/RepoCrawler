# app/query/chat_handler.py
import openai

class ChatHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def ask_chatgpt(self, question, context=""):
        """Send a question and context to the ChatGPT API and return the response, positioning the AI as a helpful assistant."""
        # Define the AI's role and explain that it should remember past interactions.
        role_description = (
            "You are a helpful assistant. Remember previous interactions during this session to provide "
            "contextually relevant responses. Here is the recent conversation history:\n"
        )
        # Build the full prompt with the role description and context
        full_prompt = f"{role_description}{context}\nYour task: {question}"
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