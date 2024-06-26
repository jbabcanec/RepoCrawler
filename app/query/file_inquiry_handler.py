import openai
import os
import re

class FileInquiryHandler:
    def __init__(self, api_key, directory_listing, repository_directory):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.repository_directory = repository_directory
        print(f"FileInquiryHandler initialized with repository_directory: {repository_directory}")  # Debug
        self.valid_files = self.parse_directory_listing(directory_listing)
        print("Valid files extracted from directory listing:", self.valid_files)

    def parse_directory_listing(self, directory_listing):
        """Parse a directory listing string to extract unique filenames."""
        lines = directory_listing.split("\n")
        filenames = set()  # Using a set to automatically handle duplicates
        for line in lines:
            filename = line.strip().rsplit(' ', 1)[-1]
            if '.' in filename:
                filenames.add(filename)  # Use 'add' instead of 'append' for a set
        return list(filenames)  # Convert set back to list if necessary for further processing

    def should_fetch_files(self, question, context, chat_history):
        """Ask GPT if specific files are necessary to enhance the answer to a question."""
        messages = [
            {"role": "system", "content": (
                "You are a helpful assistant for RepoCrawler. Utilize the detailed metadata about the project to "
                "provide informed responses about the codebase, its usage, and documentation."
            )},
            {"role": "system", "content": context},
            {"role": "user", "content": (
                f"Context: {context}\nRecent Conversations: \n{chat_history}\nGiven the comprehensive summary and keywords already provided, "
                f"and considering the specific query '{question}', is it helpful to reference specific files? "
                "Please answer 'yes' only if a code snippet or a specific function from a file is directly requested and listing the file(s) would "
                "aid in answering the query. Answer 'no' otherwise. If 'yes', list only those files that are immediately useful."
            )}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                max_tokens=500,
                temperature=0.3,
                top_p=1.0,
                n=1
            )
            response_text = response.choices[0].message['content'].strip().lower()
            # print(f'OpenAI response: {response_text}')
            needs_files = "yes" in response_text and "no" not in response_text
            files_listed = []
            file_tokens = response.usage['total_tokens']
            if needs_files:
                tentative_files = re.findall(r'\b[\w-]+?\.\w+\b', response_text)
                files_listed = self.validate_file_names(tentative_files)
            print(f'Files listed: {files_listed}')
            return needs_files, files_listed, file_tokens
        except Exception as e:
            return f"Failed to call ChatGPT API: {str(e)}", 0, 0

    def validate_file_names(self, tentative_files):
        """Ensure only unique valid filenames are listed."""
        # Use a set to deduplicate file names and filter them against valid files
        unique_files = set(file for file in tentative_files if file in self.valid_files)
        return list(unique_files)  # Convert set back to list for further processing

    def get_file_content(self, filenames):
        """Fetch the content of specified files, handling various file types."""
        content = ""
        total_tokens = 0
        for filename in filenames:
            print(f"Attempting to read: {filename} from {self.repository_directory}")  # Debug
            file_path = os.path.join(self.repository_directory, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        content += f"\n\nFile: {filename}\n{file_content}"
                        total_tokens += len(file_content.split())
                except Exception as e:
                    content += f"\n\nFile: {filename} - Error reading file: {str(e)}"
            else:
                content += f"\n\nFile: {filename} - Not Found"
        return content, total_tokens
