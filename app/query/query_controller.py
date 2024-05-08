import os
import openai
from collections import deque
from .chat_handler import ChatHandler
from .file_inquiry_handler import FileInquiryHandler

class QueryController:
    def __init__(self, data_directory='data/repo_metadata'):
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        self.api_key = self.load_api_key()
        self.file_inquiry_handler = FileInquiryHandler(self.api_key, data_directory)
        self.chat_handler = ChatHandler(self.api_key)
        self.data_directory = data_directory
        self.history_file = os.path.join(self.data_directory, 'chat_history.txt')
        self.reset_chat_history()  # Reset chat history at the start of each run
        self.chat_history = self.load_chat_history()
        self.metadata = self.load_metadata_files()

    def load_api_key(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', '..', 'credentials.txt'), 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("API Key file not found. Ensure that credentials.txt is available.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the API key: {str(e)}")

    def load_metadata_files(self):
        """Load all relevant metadata files for context enhancement."""
        metadata_files = {
            'dependencies': 'dependencies.txt',
            'directory_tree': 'directory_tree.txt',
            'document_summaries': 'document_summaries.txt',
            'keywords': 'keywords.txt',
            'summaries': 'summaries.txt'
        }
        metadata = {}
        for key, filename in metadata_files.items():
            filepath = os.path.join(self.data_directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    metadata[key] = file.read()
            except FileNotFoundError:
                metadata[key] = f"{key} information not available."
        return metadata

    def send_query(self, query):
        context = self.get_context()
        needs_files, files_needed = self.file_inquiry_handler.should_fetch_files(query, context)
        if needs_files and files_needed:
            additional_context = self.file_inquiry_handler.get_file_content(files_needed)
            context += additional_context

        quit()
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

    def reset_chat_history(self):
        """Reset the chat history file."""
        with open(self.history_file, 'w') as file:
            file.truncate()  # Clears the file if it exists, or creates it if it does not

    def store_chat_history(self, query, response):
        entry_number = len(self.chat_history) + 1
        self.chat_history.append((entry_number, "You: " + query, "Bot: " + response))
        with open(self.history_file, 'a') as file:
            file.write(f"{entry_number}. You: {query}|{entry_number}. Bot: {response}\n")

    def get_context(self):
        """Generate context from the chat history and metadata for the AI."""
        context_parts = [
            f"Dependencies:\n{self.metadata['dependencies']}",
            f"Directory Structure:\n{self.metadata['directory_tree']}",
            f"Document Summaries:\n{self.metadata['document_summaries']}",
            f"Important Keywords:\n{self.metadata['keywords']}",
            f"File Summaries:\n{self.metadata['summaries']}",
            "\n".join(f"{item[0]} {item[1]}" for item in self.chat_history)
        ]
        return "\n\n".join(context_parts)
