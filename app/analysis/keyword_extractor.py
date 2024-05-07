import os
import openai

class KeywordExtractor:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_prompt(self, file_path):
        """Create a prompt for extracting high-level keywords from the code, including the file name for context."""
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            prompt = (f"Analyze the following {file_name} code and list high-level functionalities and key concepts. "
                      f"Focus on main functionalities, important concepts, and usage of external libraries:\n\n### Code\n{content}\n### End Code")
            return prompt
        except Exception as e:
            return f"Failed to read file {file_path}: {str(e)}"

    def extract_keywords(self, prompt):
        """Send a prompt to the ChatGPT API and get high-level keywords."""
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
            keywords = response.choices[0].text.strip()
            return keywords
        except Exception as e:
            return f"Failed to call ChatGPT API: {str(e)}"

    def get_file_keywords(self, file_path):
        """Generate high-level keywords for a given file using ChatGPT."""
        prompt = self.create_prompt(file_path)
        if "Failed to read file" in prompt:
            return prompt  # Return error message if file reading fails
        return self.extract_keywords(prompt)
