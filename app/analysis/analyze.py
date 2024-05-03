# analyze.py
from app.config.settings import INCLUDE_EXTENSIONS, EXCLUDE_EXTENSIONS, EXCLUDE_DIRECTORIES
from .file_parser import find_relevant_files
from .tree import generate_directory_tree
from .summarizer import CodeSummarizer
# from .keyword_extractor import extract_keywords
# from .dependency_mapper import map_dependencies
# from .file_copier import copy_files_to_data
import os

class AnalysisController:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.api_key = self.load_api_key()
        self.summarizer = CodeSummarizer(self.api_key)
        self.data_directory = os.path.join(root_directory, "data")
        self.metadata_directory = os.path.join(self.data_directory, "repo_metadata")
        os.makedirs(self.metadata_directory, exist_ok=True)

    def load_api_key(self):
        """Loads the API key from a hard-coded relative file path."""
        api_key_path = os.path.join(os.path.dirname(__file__), '..', '..', 'credentials.txt')
        try:
            with open(api_key_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise Exception("credentials.txt file not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the API key: {str(e)}")

    def run_analysis(self):
        print("Generating directory tree...")
        directory_tree = generate_directory_tree(self.root_directory, EXCLUDE_DIRECTORIES)
        files = find_relevant_files(self.root_directory, INCLUDE_EXTENSIONS, EXCLUDE_EXTENSIONS, EXCLUDE_DIRECTORIES)
        
        print("Files considered for analysis:")
        for file_path in files:
            summary = self.summarizer.summarize_file(file_path)
            print(f"Summary for {os.path.basename(file_path)}:\n{summary}\n")

    def save_analysis_results(self, file_path, summary, keywords, dependencies):
        pass  # To be implemented