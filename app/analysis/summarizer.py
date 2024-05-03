# summarizer.py
import os
import openai

class CodeSummarizer:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_prompt(self, file_path):
        """Create a prompt for summarization including the file name for context."""
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            prompt = f"Summarize the following {file_name} code in terms of its functionality:\n\n### Code\n{content}\n### End Code"
            return prompt
        except Exception as e:
            return f"Failed to read file {file_path}: {str(e)}"

    def summarize_code_with_chatgpt(self, prompt):
        """Send a prompt to the ChatGPT API and get the summary."""
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=150,
                temperature=0.5,
                top_p=1.0,
                n=1,
                stop=["### End Code"],
                api_key=self.api_key
            )
            summary = response.choices[0].text.strip()
            return summary
        except Exception as e:
            return f"Failed to call ChatGPT API: {str(e)}"

    def summarize_file(self, file_path):
        """Generate a summary for a given file using ChatGPT."""
        prompt = self.create_prompt(file_path)
        if "Failed to read file" in prompt:
            return prompt
        return self.summarize_code_with_chatgpt(prompt)
