import os

def find_relevant_files(root_directory, include_extensions, exclude_extensions, exclude_directories):
    """
    Traverse the directory tree starting from root_directory to find files that match the
    inclusion criteria and do not match the exclusion criteria.
    """
    relevant_files = []
    for root, dirs, files in os.walk(root_directory, topdown=True):
        # Modify the dirs in-place to exclude unwanted directories during traversal
        dirs[:] = [d for d in dirs if d not in exclude_directories]

        for file in files:
            # Check file extension against included and excluded extensions
            _, ext = os.path.splitext(file)
            if ext in include_extensions and ext not in exclude_extensions:
                full_path = os.path.join(root, file)
                relevant_files.append(full_path)

    return relevant_files
