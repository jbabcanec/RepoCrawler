import git
import os

def clone_repository(repo_url):
    # Get the directory of the currently running script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    destination_folder = os.path.join(current_directory, "cloned_repo")  # You can customize the folder name

    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Attempt to clone the repository
    try:
        git.Repo.clone_from(repo_url, destination_folder)
        print(f"Repository cloned successfully to {destination_folder}")
    except Exception as e:
        print(f"An error occurred while cloning the repository: {e}")

# Example Usage
repo_url = 'https://github.com/jbabcanec/DayMaker.git'  # Replace with the actual repository URL
clone_repository(repo_url)
