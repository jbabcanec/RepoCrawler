import os
import openai

class DependencyMapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.graph = {}

    def create_dependency_prompt(self, file_path, file_content, directory_tree):
        """Create a prompt to identify script-to-script relationships based on the code content."""
        prompt = (
            f"Given the directory structure:\n{directory_tree}\n\n"
            f"Analyze the following code from '{file_path}'. List any direct function calls or interactions "
            f"between this script and other scripts in the project. Provide the relationships in the format "
            f"'script1 calls functions from script2':\n\n### Code\n{file_content}\n### End Code"
        )
        return prompt

    def extract_dependencies(self, prompt):
        """Send a prompt to the ChatGPT API and parse the dependencies into a graph."""
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=300,
                temperature=0.3,
                top_p=1.0,
                n=1,
                stop=["### End Code"],
                api_key=self.api_key
            )
            dependencies = response.choices[0].text.strip()
            return dependencies.split('\n')
        except Exception as e:
            return [f"Failed to call ChatGPT API: {str(e)}"]

    def update_graph(self, dependencies, source_script):
        """Update the graph with dependencies, focusing on script-to-script relationships."""
        self.graph[source_script] = []
        for dependency in dependencies:
            if 'calls functions from' in dependency:
                parts = dependency.split('calls functions from')
                if len(parts) > 1:
                    target_script = parts[1].strip()
                    if target_script and target_script != source_script:  # Ensure no self-references
                        self.graph[source_script].append(target_script)

    def map_file_dependencies(self, file_path, file_content, directory_tree):
        """Generate a dependency map for a given file using ChatGPT and update the graph."""
        prompt = self.create_dependency_prompt(file_path, file_content, directory_tree)
        dependencies = self.extract_dependencies(prompt)
        self.update_graph(dependencies, os.path.basename(file_path))
        return dependencies

    def get_dependencies(self):
        """Return the dependencies in a readable format."""
        dependencies_str = "Script Dependencies:\n"
        for script, deps in self.graph.items():
            if deps:
                dependencies_str += f"{script} -> {', '.join(deps)}\n"
            else:
                dependencies_str += f"{script} has no script dependencies.\n"
        return dependencies_str
