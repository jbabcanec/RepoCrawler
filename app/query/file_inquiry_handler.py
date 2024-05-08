import openai
import os
import re

class FileInquiryHandler:
    def __init__(self, api_key, data_directory):
        self.api_key = api_key
        self.data_directory = data_directory

    def should_fetch_files(self, question, context):
        """Ask GPT if specific files are necessary to enhance the answer to a question."""
        prompt = (f"{context}\nGiven the comprehensive summary and keywords already provided, "
                  f"is it very strictly necessary to reference specific files to answer the query '{question}'? "
                  "Please conservatively answer only 'yes' or 'no' and list the files if 'yes' only if absolutely essential. "
                  "We want to use the minimum amount of files to contextualize as possible. Do not provide files if answer is 'no'")
        print(f'prompt: {prompt}')
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500,
            temperature=0.3,
            top_p=1.0,
            n=1,
            stop=None,
            api_key=self.api_key
        )
        response_text = response.choices[0].text.strip().lower()
        print(f'response: {response_text}')
        needs_files = "yes" in response_text and "no" not in response_text  # Ensures 'no' is prioritized if both are mentioned
        files_listed = []
        if needs_files:
            files_listed = re.findall(r'\b[\w\s-]+\.\w+\b', response_text)
        print(files_listed)
        return needs_files, files_listed

    def get_file_content(self, filenames):
        """Fetch the content of specified files, handling various file types."""
        content = ""
        for filename in filenames:
            file_path = os.path.join(self.data_directory, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content += f"\n\nFile: {filename}\n{file.read()}"
                except Exception as e:
                    content += f"\n\nFile: {filename} - Error reading file: {str(e)}"
            else:
                content += f"\n\nFile: {filename} - Not Found"
        return content