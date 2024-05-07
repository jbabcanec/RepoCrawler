from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config.settings import *
from .file_parser import find_relevant_files
from .tree import generate_directory_tree
from .code_summarizer import CodeSummarizer
from .keyword_extractor import KeywordExtractor
from .dependency_mapper import DependencyMapper
import os

class AnalysisController:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.api_key = self.load_api_key()
        self.summarizer = CodeSummarizer(self.api_key)
        self.keyword_extractor = KeywordExtractor(self.api_key)
        self.dependency_mapper = DependencyMapper(self.api_key)

        self.data_directory = os.path.join(os.path.dirname(root_directory), "repo_metadata")
        os.makedirs(self.data_directory, exist_ok=True)

    def load_api_key(self):
        api_key_path = os.path.join(os.path.dirname(__file__), '..', '..', 'credentials.txt')
        try:
            with open(api_key_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise Exception("credentials.txt file not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the API key: {str(e)}")

    def run_analysis(self):
        directory_tree = generate_directory_tree(self.root_directory, EXCLUDE_DIRECTORIES)
        self.save_text_file('directory_tree.txt', str(directory_tree))

        files = find_relevant_files(self.root_directory, INCLUDE_EXTENSIONS, EXCLUDE_EXTENSIONS, EXCLUDE_DIRECTORIES)
        summaries = []
        keywords_list = []

        with ThreadPoolExecutor(max_workers=16) as executor:
            future_to_file = {executor.submit(self.process_file, file_path, directory_tree): file_path for file_path in files}
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_results = future.result()
                    summaries.append(f"Processed file: {os.path.basename(file_path)}\nSummary: {file_results['summary']}")
                    if isinstance(file_results['keywords'], list):
                        formatted_keywords = ', '.join(file_results['keywords'])
                    else:
                        formatted_keywords = file_results['keywords']
                    keywords_list.append(f"Processed file: {os.path.basename(file_path)}\nKeywords: {formatted_keywords}")
                except Exception as e:
                    print(f'Exception processing file {file_path}: {e}')

        self.save_text_file('summaries.txt', "\n".join(summaries))
        self.save_text_file('keywords.txt', "\n".join(keywords_list))

        # Save dependencies after all files have been processed
        dependencies = self.dependency_mapper.get_dependencies()
        self.save_text_file('dependencies.txt', dependencies)

    def process_file(self, file_path, directory_tree):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        summary = self.summarizer.summarize_file(file_path)
        keywords = self.keyword_extractor.get_file_keywords(file_path)
        self.dependency_mapper.map_file_dependencies(file_path, content, directory_tree)
        return {'summary': summary, 'keywords': keywords}

    def save_text_file(self, file_name, content):
        path = os.path.join(self.data_directory, file_name)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
