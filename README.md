
# RepoCrawler

**RepoCrawler** is a powerful tool designed to analyze and map out the structure of software repositories. This application is built using PyQt5 and integrates OpenAI's GPT model to provide detailed insights into code bases, documentation, and repository structure. The main functionalities include uploading and cloning repositories, analyzing their content, visualizing directory structures, and querying specific details about the repository components.

## Key Features

-   **Upload Repository**: Allows users to upload local repositories for analysis.
-   **Clone Repository**: Users can clone repositories from remote locations such as GitHub.
-   **Analyze Repository**: Performs an in-depth analysis of the repository files, filtering by type and relevance, and provides a summary of each file.
-   **Map Directory Structure**: Visually maps the directory structure of the repository excluding specified directories.
-   **Query Information**: After analysis, users can query specific information about the repository structure and contents.

## Installation Requirements

**RepoCrawler** requires the following environment and libraries:

-   **Python**: Version 3.6 or later.
-   **PyQt5**: For the graphical user interface.
-   **GitPython**: For handling git operations if cloning functionality is used.

To set up the environment and install the required packages, follow these steps:

1.  **Python Installation**: Ensure Python 3.6 or later is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
    
2.  **Virtual Environment** (optional but recommended): Create a virtual environment to keep dependencies required by different projects separate by running:
    
    Copy code
    
    `python -m venv venv` 
    
    Activate the virtual environment:
    
    -   Windows: `venv\Scripts\activate`
    -   macOS/Linux: `source venv/bin/activate`
3.  **Install Dependencies**: Install all required packages using pip:
    
    Copy code
    
    `pip install PyQt5 GitPython` 
    

## Configuration

Before running the application, configure the settings in `app/config/settings.py` to specify which file types and directories should be included or excluded from analysis.

### Running the Application

To start the application, navigate to the project directory in your terminal and run:

`python main.py` 

This will launch the GUI where you can start interacting with the application.

### Usage

1.  **Uploading a Repository**:
    
    -   Click on "Upload Repository" and select the directory of your local repository.
    -   Once uploaded, the "Analyze" and "Map" buttons will be enabled.
2.  **Cloning a Repository**:
    
    -   Click on "Clone Repository".
    -   Enter the repository URL and start the cloning process.
    -   Similar to upload, this will enable further analysis and mapping options.
3.  **Analyzing the Repository**:
    
    -   Click "Analyze Repository" to start the analysis process.
    -   Upon completion, you can query the repository for detailed information.
4.  **Mapping the Directory Structure**:
    
    -   Click "Show Map" to visualize the repository's directory structure in a structured tree format.
5.  **Querying the Repository**:
    
    -   Once analysis is done, use the "Query" button to perform specific searches within the repository data.