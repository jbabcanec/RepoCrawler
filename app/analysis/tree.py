import os

def generate_directory_tree(root_directory, exclude_directories, prefix=''):
    """ Generate a directory tree structure as a string """
    # Files and directories at the current directory level
    items = os.listdir(root_directory)
    items = sorted(items)  # Sort to maintain alphabetical order
    if not items:
        return ''  # Return empty string if no items to process

    # Filter to exclude specified directories
    items = [item for item in items if item not in exclude_directories]

    # Structure lines
    lines = []
    for i, item in enumerate(items):
        item_path = os.path.join(root_directory, item)
        if os.path.isdir(item_path):
            # Handle subdirectory; check for last item to choose the correct prefix
            if i == len(items) - 1:
                lines.append(f"{prefix}└── {item}")
                extension = generate_directory_tree(item_path, exclude_directories, prefix + "    ")
            else:
                lines.append(f"{prefix}├── {item}")
                extension = generate_directory_tree(item_path, exclude_directories, prefix + "│   ")
            lines.append(extension)
        else:
            # Handle files; check if last item to choose the correct prefix
            if i == len(items) - 1:
                lines.append(f"{prefix}└── {item}")
            else:
                lines.append(f"{prefix}├── {item}")

    return "\n".join(lines)