# document_summarizer.py
import os
import openai

class DocumentSummarizer:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_prompt(self, file_path):
        """Create a prompt for summarization including the file name for context, requesting a hyper-compressed summary."""
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Update the prompt to specify the need for a highly compressed summary
            prompt = (f"Provide a highly concise summary of the following documentation ({file_name}), "
                      f"focusing strictly on critical functionalities:\n\n{content}")
            return prompt
        except Exception as e:
            return f"Failed to read file {file_path}: {str(e)}"

    def summarize_document_with_chatgpt(self, prompt):
        """Send a prompt to the ChatGPT API and get the summary."""
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=300,  # Adjust token limit as needed for more detailed summaries
                temperature=0.3,  # Lower temperature for more focused output
                top_p=1.0,
                n=1,
                stop=None,
                api_key=self.api_key
            )
            summary = response.choices[0].text.strip()
            return summary
        except Exception as e:
            return f"Failed to call ChatGPT API: {str(e)}"

    def summarize_file(self, file_path):
        """Generate a summary for a given document file."""
        prompt = self.create_prompt(file_path)
        if "Failed to read file" in prompt:
            return prompt
        return self.summarize_document_with_chatgpt(prompt)
