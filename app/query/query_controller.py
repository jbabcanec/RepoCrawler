import os
import openai
from collections import deque
from .chat_handler import ChatHandler

class QueryController:
    def __init__(self, data_directory='data/repo_metadata'):
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        self.api_key = self.load_api_key()
        self.chat_handler = ChatHandler(self.api_key)
        self.data_directory = data_directory
        self.history_file = os.path.join(self.data_directory, 'chat_history.txt')
        self.chat_history = self.load_chat_history()

    def load_api_key(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', '..', 'credentials.txt'), 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("API Key file not found. Ensure that credentials.txt is available.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the API key: {str(e)}")

    def send_query(self, query):
        context = self.get_context()
        response = self.chat_handler.ask_chatgpt(query, context)
        self.store_chat_history(query, response)
        return response

    def load_chat_history(self):
        try:
            with open(self.history_file, 'r') as file:
                history_lines = file.readlines()
            return deque([tuple(line.strip().split('|')) for line in history_lines], maxlen=50)
        except FileNotFoundError:
            return deque(maxlen=50)

    def store_chat_history(self, query, response):
        entry_number = len(self.chat_history) + 1
        self.chat_history.append((entry_number, "You: " + query, "Bot: " + response))
        with open(self.history_file, 'a') as file:
            file.write(f"{entry_number}. You: {query}|{entry_number}. Bot: {response}\n")

    def get_context(self):
        context_lines = [" ".join(str(item) for item in pair) for pair in self.chat_history]
        return "\n".join(context_lines)
