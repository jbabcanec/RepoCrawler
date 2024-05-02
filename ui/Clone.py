from PyQt5 import QtWidgets, QtCore
import git
import os

def clone_repository(repo_url, destination_folder, callback):
    try:
        # Ensure the repository URL ends with ".git"
        if not repo_url.endswith(".git"):
            repo_url += ".git"
        # Clone the repository
        git.Repo.clone_from(repo_url, destination_folder)
        callback(True, f"Repository cloned successfully to {destination_folder}")  # Callback to signal success
    except Exception as e:
        callback(False, f"An error occurred while cloning the repository: {e}")  # Callback to signal failure

class CloneRepoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, callback=None):
        super(CloneRepoDialog, self).__init__(parent)
        self.callback = callback  # Store the callback function passed from MainWindow

        self.setWindowTitle("Clone Repository")
        self.setFixedSize(400, 120)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())
        # Set window icon
        self.setWindowIcon(QtGui.QIcon('./resources/crawler.ico'))

        layout = QtWidgets.QVBoxLayout(self)
        
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setPlaceholderText("Enter GitHub repository URL...")
        layout.addWidget(self.lineEdit)
        
        clone_button = QtWidgets.QPushButton("Clone", self)
        clone_button.clicked.connect(self.start_cloning)
        layout.addWidget(clone_button)

    def start_cloning(self):
        repo_url = self.lineEdit.text()
        # Automatically append '.git' if not present
        if not repo_url.endswith(".git"):
            repo_url += ".git"
        
        project_name = os.path.basename(repo_url[:-4])  # Remove '.git' and get the repository name
        current_directory = os.path.dirname(os.path.abspath(__file__))
        destination_folder = os.path.join(current_directory, "../data", f"{project_name}_repo")
        
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        clone_repository(repo_url, destination_folder, self.clone_finished)

    def clone_finished(self, success, message):
        if success:
            self.callback(destination_folder)  # Use the destination folder path if cloning is successful
            QtWidgets.QMessageBox.information(self, "Clone Successful", message)
            self.accept()  # Close the dialog on successful cloning
        else:
            self.callback(None)  # Pass None if cloning failed
            QtWidgets.QMessageBox.critical(self, "Clone Failed", message)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = CloneRepoDialog()
    dlg.show()
    sys.exit(app.exec_())
