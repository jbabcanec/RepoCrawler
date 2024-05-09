import openai
import os
import re

class FileInquiryHandler:
    def __init__(self, api_key, directory_listing):
        self.api_key = api_key
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
        prompt = (f"Context: {context}\nRecent Conversations: \n{chat_history}\nGiven the comprehensive summary and keywords already provided, "
                  f"and considering the specific query '{question}', is it helpful to reference specific files? "
                  "Please answer 'yes' only if a code snippet or a specific function from a file is directly requested and listing the file(s) would "
                  "aid in answering the query. Answer 'no' otherwise. If 'yes', list only those files that are immediately useful.")
        
        #print(f'Prompt for OpenAI: {prompt}')
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
        print(f'OpenAI response: {response_text}')
        needs_files = "yes" in response_text and "no" not in response_text
        files_listed = []
        if needs_files:
            tentative_files = re.findall(r'\b[\w-]+?\.\w+\b', response_text)
            files_listed = self.validate_file_names(tentative_files)
        print(f'Files listed: {files_listed}')
        return needs_files, files_listed

    def validate_file_names(self, tentative_files):
        """Ensure only unique valid filenames are listed."""
        # Use a set to deduplicate file names and filter them against valid files
        unique_files = set(file for file in tentative_files if file in self.valid_files)
        return list(unique_files)  # Convert set back to list for further processing

    def get_file_content(self, filenames):
        """Fetch the content of specified files, handling various file types."""
        content = ""
        for filename in filenames:
            content += f"\n\nFile: {filename}\n(Content of {filename})"
        return content