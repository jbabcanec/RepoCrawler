# analyze.py
from app.config.settings import INCLUDE_EXTENSIONS, EXCLUDE_EXTENSIONS, EXCLUDE_DIRECTORIES
from .file_parser import find_relevant_files
from .tree import generate_directory_tree
# from .summarizer import summarize_code
# from .keyword_extractor import extract_keywords
# from .dependency_mapper import map_dependencies
# from .file_copier import copy_files_to_data
import os

class AnalysisController:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.data_directory = os.path.join(root_directory, "data")

    def run_analysis(self):
        print("Generating directory tree...")
        directory_tree = generate_directory_tree(self.root_directory, EXCLUDE_DIRECTORIES)
        print(directory_tree)  # Print the directory tree

        # Use settings from the configuration file
        files = find_relevant_files(self.root_directory, INCLUDE_EXTENSIONS, EXCLUDE_EXTENSIONS, EXCLUDE_DIRECTORIES)

        # Step 2: Process each file
        print("Files considered for analysis:")
        for file_path in files:
            print(file_path)  # Just print out the file paths being considered
            # # Comment out the processing steps
            # summary = summarize_code(file_path)
            # keywords = extract_keywords(summary)
            # dependencies = map_dependencies(file_path)
            # Optionally print or save the analysis results
            # self.save_analysis_results(file_path, summary, keywords, dependencies)

        # Step 3: Comment out copying as we're just listing files for now
        # copy_files_to_data(self.root_directory, self.data_directory, INCLUDE_EXTENSIONS)

    def save_analysis_results(self, file_path, summary, keywords, dependencies):
        # This is also commented out for now as we are not processing files
        pass
