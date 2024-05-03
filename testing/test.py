# tests/test.py
import sys
import os

# Adjust the path to include the root directory so we can import modules from 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.analysis.analyze import AnalysisController

def main():
    # Define the path to the repository to be analyzed
    # Assume the test repo is directly under the 'data' directory in the root of your project
    root_directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'DayMaker_repo')

    # Create an instance of AnalysisController with just the repository path
    analysis_controller = AnalysisController(root_directory)
    
    # Run the analysis
    analysis_controller.run_analysis()
    print("Analysis complete!")

if __name__ == "__main__":
    main()
