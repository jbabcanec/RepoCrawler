from PyQt5 import QtWidgets, QtGui, QtCore
from app.query.query_controller import QueryController
import time

class QueryDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, repository_directory=None):
        super(QueryDialog, self).__init__(parent)
        self.setWindowTitle("Query Chatbot")
        self.resize(600, 400)
        print(f"QueryDialog initialized with repository_directory: {repository_directory}")  # Debug
        self.query_controller = QueryController(repository_directory=repository_directory)

        layout = QtWidgets.QVBoxLayout(self)

        # Token and Timer Information
        self.infoLayout = QtWidgets.QHBoxLayout()
        self.tokenLabel = QtWidgets.QLabel("Tokens: 0", self)
        self.timeLabel = QtWidgets.QLabel("Time: 0s", self)
        self.tokensPerMinuteLabel = QtWidgets.QLabel("Tokens/Minute: 0", self)
        self.infoLayout.addWidget(self.tokenLabel)
        self.infoLayout.addWidget(self.timeLabel)
        self.infoLayout.addWidget(self.tokensPerMinuteLabel)
        layout.addLayout(self.infoLayout)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet("background-color: #f0f0f0; font-family: Arial; font-size: 14px;")

        self.inputLine = QtWidgets.QLineEdit(self)
        self.inputLine.setPlaceholderText("Ask a question...")
        self.inputLine.returnPressed.connect(self.process_query)

        self.sendButton = QtWidgets.QPushButton("Send", self)
        self.sendButton.clicked.connect(self.process_query)

        layout.addWidget(self.textEdit)
        layout.addWidget(self.inputLine)
        layout.addWidget(self.sendButton)

        self.startTime = 0
        self.totalTokens = 0

    def process_query(self):
        query_text = self.inputLine.text().strip()
        if query_text:
            self.append_message(f"You: {query_text}")
            self.show_loading_message("Waiting for response...")

            QtWidgets.QApplication.processEvents()  # Update UI to show loading message

            # Start the timer
            self.startTime = time.time()

            response_text, token_count = self.query_controller.send_query(query_text)

            # Stop the timer
            elapsed_time = time.time() - self.startTime
            tokens_per_minute = (token_count / elapsed_time) * 60 if elapsed_time > 0 else 0

            # Update the UI elements
            self.totalTokens += token_count
            self.tokenLabel.setText(f"Tokens: {self.totalTokens}")
            self.timeLabel.setText(f"Time: {elapsed_time:.2f}s")
            self.tokensPerMinuteLabel.setText(f"Tokens/Minute: {tokens_per_minute:.2f}")

            # Formatting the response based on content
            formatted_response = self.format_response(response_text)

            self.append_html_message(formatted_response)  # Using HTML to format the response with a separator
            self.inputLine.clear()

    def append_message(self, message):
        self.textEdit.append(message)
        self.textEdit.ensureCursorVisible()

    def append_html_message(self, html_message):
        self.textEdit.append(html_message)
        self.textEdit.ensureCursorVisible()

    def format_response(self, response_text):
        """Format the response text with HTML for better readability, including separators."""
        separator = "<hr style='border:1px solid #ccc; margin: 10px 0;'/>"  # Separator for clarity
        if "<code>" in response_text:
            response_html = f"<pre style='font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; background-color:#f7f7f7; padding:5px; margin:10px 0;'>{response_text}</pre>"
        else:
            response_html = f"<div style='margin: 10px 0;'>{response_text}</div>"
        return separator + response_html  # Append separator before the formatted response

    def show_loading_message(self, message):
        """Show a loading message in the chat while waiting for a response."""
        self.textEdit.append(f"<i style='color:gray;'>{message}</i>")
