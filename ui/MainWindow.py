from PyQt5 import QtCore, QtWidgets, QtGui
from ui.Clone import CloneRepoDialog
from ui.Query import QueryDialog
from app.analysis.analyze import AnalysisController

import os
import shutil

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.resize(285, 280)  # Ensure there's enough space for all UI components
        self.current_repository_folder = None
        
        # Set window icon
        self.setWindowIcon(QtGui.QIcon('./resources/crawler.ico'))
        
        # Create a label to display the image, adjusted size and position
        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setGeometry(QtCore.QRect(112, 10, 60, 60))  # Center the image, adjust position
        pixmap = QtGui.QPixmap("./resources/crawler.png")
        self.imageLabel.setPixmap(pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio))
        
        # Create a label for the text "RepoCrawler"
        self.titleLabel = QtWidgets.QLabel("RepoCrawler", self)
        self.titleLabel.setGeometry(QtCore.QRect(80, 80, 125, 20))  # Position under the image, centered
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        # Setup buttons
        self.uploadButton = QtWidgets.QPushButton("Upload Repository", self)
        self.uploadButton.setGeometry(QtCore.QRect(80, 110, 121, 23))
        
        self.cloneRepoButton = QtWidgets.QPushButton("Clone Repository", self)
        self.cloneRepoButton.setGeometry(QtCore.QRect(80, 140, 121, 23))
        
        self.analyzeButton = QtWidgets.QPushButton("Analyze Repository", self)
        self.analyzeButton.setGeometry(QtCore.QRect(80, 170, 121, 23))
        
        self.mapButton = QtWidgets.QPushButton("Show Map", self)
        self.mapButton.setGeometry(QtCore.QRect(80, 200, 121, 23))
        
        self.queryButton = QtWidgets.QPushButton("Query", self)
        self.queryButton.setGeometry(QtCore.QRect(80, 240, 121, 23))
        #self.queryButton.setEnabled(False)  # Initially disabled
        #we enable the query button for debugging purposes so we are not required to read in or clone a repo, 
        #instead we just use the repo sitting in the folder

        # Connect signals
        self.uploadButton.clicked.connect(self.upload_repository)
        self.cloneRepoButton.clicked.connect(self.show_clone_repo_dialog)
        self.analyzeButton.clicked.connect(self.analyze_repository)
        self.mapButton.clicked.connect(self.show_map)
        self.queryButton.clicked.connect(self.query_repository)

        # Initially disable analyze and map buttons
        self.analyzeButton.setEnabled(False)
        self.mapButton.setEnabled(False)

        # Set the initial UI translations
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "RepoCrawler"))
        self.uploadButton.setText(_translate("MainWindow", "Upload Repository"))
        self.cloneRepoButton.setText(_translate("MainWindow", "Clone Repository"))
        self.analyzeButton.setText(_translate("MainWindow", "Analyze Repository"))
        self.mapButton.setText(_translate("MainWindow", "Show Map"))
        self.queryButton.setText(_translate("MainWindow", "Query"))

    def upload_repository(self):
        source_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Repository Folder')
        if source_folder:
            project_name = os.path.basename(source_folder)
            current_directory = os.path.dirname(os.path.abspath(__file__))
            destination_folder = os.path.join(current_directory, "../data", f"{project_name}_repo")
            
            if os.path.exists(destination_folder):
                shutil.rmtree(destination_folder)  # Clear existing directory first
            os.makedirs(destination_folder)
            
            # Copy all files and directories from source to destination
            try:
                for item in os.listdir(source_folder):
                    s = os.path.join(source_folder, item)
                    d = os.path.join(destination_folder, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)

                self.current_repository_folder = destination_folder
                self.analyzeButton.setEnabled(True)
                self.mapButton.setEnabled(True)
                QtWidgets.QMessageBox.information(self, "Upload Successful", f"Files copied successfully to {destination_folder}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Upload Failed", f"Failed to copy files: {str(e)}")
                self.current_repository_folder = None
        else:
            QtWidgets.QMessageBox.warning(self, "Upload Canceled", "No folder selected.")

    def show_clone_repo_dialog(self):
        self.dialog = CloneRepoDialog(self, callback=self.update_repository_folder)
        self.dialog.show()

    def update_repository_folder(self, folder_path):
        if folder_path:
            self.current_repository_folder = folder_path
            print(f"Repository folder updated to: {self.current_repository_folder}")  # Debug statement
            self.analyzeButton.setEnabled(True)
            self.mapButton.setEnabled(True)
            QtWidgets.QMessageBox.information(self, "Clone Successful", "Repository cloned and ready for analysis.")
        else:
            QtWidgets.QMessageBox.warning(self, "Clone Failed", "The repository could not be cloned.")

    def analyze_repository(self):
        if self.current_repository_folder:
            try:
                analyzer = AnalysisController(self.current_repository_folder)
                analyzer.run_analysis()
                QtWidgets.QMessageBox.information(self, "Analysis Complete", "The repository has been successfully analyzed.")
                self.queryButton.setEnabled(True)  # Enable query button after successful analysis
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Analysis Failed", f"An error occurred during analysis: {str(e)}")
                self.queryButton.setEnabled(False)
        else:
            QtWidgets.QMessageBox.warning(self, "No Repository", "Please upload or clone a repository first.")

    def show_map(self):
        print("Show map clicked")
        self.queryButton.setEnabled(True)  # Enable query button after showing map

    def query_repository(self):
        # Pass the current_repository_folder to the QueryDialog
        self.queryDialog = QueryDialog(self, self.current_repository_folder)
        self.queryDialog.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
