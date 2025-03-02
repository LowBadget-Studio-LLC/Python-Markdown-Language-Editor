import sys
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QTextBrowser,
    QToolBar, QAction, QFileDialog, QMenuBar
)
from PyQt5.QtCore import Qt


class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Python Markdown Language Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create a splitter to divide the editor and preview
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Markdown editor (left side)
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your Markdown here...")
        self.editor.textChanged.connect(self.update_preview)
        splitter.addWidget(self.editor)

        # Markdown preview (right side)
        self.preview = QTextBrowser()
        splitter.addWidget(self.preview)

        # Set initial sizes for the splitter
        splitter.setSizes([400, 400])

        # Initialize preview
        self.update_preview()

        # Add menu bar
        self.add_menubar()

        # Add status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Words: 0")

        # Listen to editor content changes to update word count
        self.editor.textChanged.connect(self.update_word_count)

    def add_menubar(self):
        """Add menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Open file
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save file
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Export menu
        export_menu = menubar.addMenu("Export")

        # Export to HTML
        export_html_action = QAction("Export to HTML", self)
        export_html_action.triggered.connect(self.export_html)
        export_menu.addAction(export_html_action)

        # Theme menu
        theme_menu = menubar.addMenu("Theme")

        # Add 20 themes
        themes = [
            ("Light Theme", "light"),
            ("Dark Theme", "dark"),
            ("Green Theme", "green"),
            ("Purple Theme", "purple"),
            ("Blue Theme", "blue"),
            ("Solarized Light", "solarized_light"),
            ("Solarized Dark", "solarized_dark"),
            ("Monokai", "monokai"),
            ("Dracula", "dracula"),
            ("Nord", "nord"),
            ("Gruvbox Light", "gruvbox_light"),
            ("Gruvbox Dark", "gruvbox_dark"),
            ("One Dark", "one_dark"),
            ("One Light", "one_light"),
            ("Material Dark", "material_dark"),
            ("Material Light", "material_light"),
            ("Retro", "retro"),
            ("Cyberpunk", "cyberpunk"),
            ("Ocean", "ocean"),
            ("Forest", "forest"),
        ]

        for theme_name, theme_id in themes:
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, id=theme_id: self.apply_theme(id))
            theme_menu.addAction(action)

    def update_preview(self):
        """Update the preview pane with rendered Markdown"""
        markdown_text = self.editor.toPlainText()
        html = markdown.markdown(
            markdown_text,
            extensions=[
                CodeHiliteExtension(linenums=False, css_class="highlight"),
                FencedCodeExtension(),
            ],
        )
        self.preview.setHtml(html)

    def open_file(self):
        """Open a Markdown file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md);;All Files (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.editor.setPlainText(file.read())

    def save_file(self):
        """Save the Markdown file"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Markdown File", "", "Markdown Files (*.md);;All Files (*)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())

    def export_html(self):
        """Export the Markdown content as an HTML file"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export HTML File", "", "HTML Files (*.html);;All Files (*)")
        if file_path:
            markdown_text = self.editor.toPlainText()
            html = markdown.markdown(markdown_text)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html)

    def update_word_count(self):
        """Update the word count in the status bar"""
        text = self.editor.toPlainText()
        word_count = len(text.split())
        self.status_bar.showMessage(f"Words: {word_count}")

    def apply_theme(self, theme_name):
        """Apply a theme"""
        themes = {
            "light": {
                "stylesheet": "",
                "editor_bg": "#FFFFFF",
                "editor_fg": "#000000",
                "preview_bg": "#FFFFFF",
                "preview_fg": "#000000",
            },
            "dark": {
                "stylesheet": """
                QWidget {
                    background-color: #2E3440;
                    color: #D8DEE9;
                }
                QTextEdit {
                    background-color: #3B4252;
                    color: #E5E9F0;
                }
                QTextBrowser {
                    background-color: #3B4252;
                    color: #E5E9F0;
                }
                """,
                "editor_bg": "#3B4252",
                "editor_fg": "#E5E9F0",
                "preview_bg": "#3B4252",
                "preview_fg": "#E5E9F0",
            },
            "green": {
                "stylesheet": """
                QWidget {
                    background-color: #F0FFF0;
                    color: #006400;
                }
                QTextEdit {
                    background-color: #E0FFE0;
                    color: #004400;
                }
                QTextBrowser {
                    background-color: #E0FFE0;
                    color: #004400;
                }
                """,
                "editor_bg": "#E0FFE0",
                "editor_fg": "#004400",
                "preview_bg": "#E0FFE0",
                "preview_fg": "#004400",
            },
            "purple": {
                "stylesheet": """
                QWidget {
                    background-color: #2E2E3A;
                    color: #D8D8E9;
                }
                QTextEdit {
                    background-color: #3B3B4A;
                    color: #E5E5F0;
                }
                QTextBrowser {
                    background-color: #3B3B4A;
                    color: #E5E5F0;
                }
                """,
                "editor_bg": "#3B3B4A",
                "editor_fg": "#E5E5F0",
                "preview_bg": "#3B3B4A",
                "preview_fg": "#E5E5F0",
            },
            "blue": {
                "stylesheet": """
                QWidget {
                    background-color: #E6F7FF;
                    color: #003366;
                }
                QTextEdit {
                    background-color: #D1E9FF;
                    color: #002244;
                }
                QTextBrowser {
                    background-color: #D1E9FF;
                    color: #002244;
                }
                """,
                "editor_bg": "#D1E9FF",
                "editor_fg": "#002244",
                "preview_bg": "#D1E9FF",
                "preview_fg": "#002244",
            },
            "solarized_light": {
                "stylesheet": """
                QWidget {
                    background-color: #FDF6E3;
                    color: #657B83;
                }
                QTextEdit {
                    background-color: #EEE8D5;
                    color: #586E75;
                }
                QTextBrowser {
                    background-color: #EEE8D5;
                    color: #586E75;
                }
                """,
                "editor_bg": "#EEE8D5",
                "editor_fg": "#586E75",
                "preview_bg": "#EEE8D5",
                "preview_fg": "#586E75",
            },
            "solarized_dark": {
                "stylesheet": """
                QWidget {
                    background-color: #002B36;
                    color: #839496;
                }
                QTextEdit {
                    background-color: #073642;
                    color: #93A1A1;
                }
                QTextBrowser {
                    background-color: #073642;
                    color: #93A1A1;
                }
                """,
                "editor_bg": "#073642",
                "editor_fg": "#93A1A1",
                "preview_bg": "#073642",
                "preview_fg": "#93A1A1",
            },
            "monokai": {
                "stylesheet": """
                QWidget {
                    background-color: #272822;
                    color: #F8F8F2;
                }
                QTextEdit {
                    background-color: #3E3D32;
                    color: #F8F8F2;
                }
                QTextBrowser {
                    background-color: #3E3D32;
                    color: #F8F8F2;
                }
                """,
                "editor_bg": "#3E3D32",
                "editor_fg": "#F8F8F2",
                "preview_bg": "#3E3D32",
                "preview_fg": "#F8F8F2",
            },
            "dracula": {
                "stylesheet": """
                QWidget {
                    background-color: #282A36;
                    color: #F8F8F2;
                }
                QTextEdit {
                    background-color: #44475A;
                    color: #F8F8F2;
                }
                QTextBrowser {
                    background-color: #44475A;
                    color: #F8F8F2;
                }
                """,
                "editor_bg": "#44475A",
                "editor_fg": "#F8F8F2",
                "preview_bg": "#44475A",
                "preview_fg": "#F8F8F2",
            },
            "nord": {
                "stylesheet": """
                QWidget {
                    background-color: #2E3440;
                    color: #D8DEE9;
                }
                QTextEdit {
                    background-color: #3B4252;
                    color: #E5E9F0;
                }
                QTextBrowser {
                    background-color: #3B4252;
                    color: #E5E9F0;
                }
                """,
                "editor_bg": "#3B4252",
                "editor_fg": "#E5E9F0",
                "preview_bg": "#3B4252",
                "preview_fg": "#E5E9F0",
            },
            "gruvbox_light": {
                "stylesheet": """
                QWidget {
                    background-color: #FBF1C7;
                    color: #3C3836;
                }
                QTextEdit {
                    background-color: #EBDBB2;
                    color: #3C3836;
                }
                QTextBrowser {
                    background-color: #EBDBB2;
                    color: #3C3836;
                }
                """,
                "editor_bg": "#EBDBB2",
                "editor_fg": "#3C3836",
                "preview_bg": "#EBDBB2",
                "preview_fg": "#3C3836",
            },
            "gruvbox_dark": {
                "stylesheet": """
                QWidget {
                    background-color: #282828;
                    color: #EBDBB2;
                }
                QTextEdit {
                    background-color: #3C3836;
                    color: #EBDBB2;
                }
                QTextBrowser {
                    background-color: #3C3836;
                    color: #EBDBB2;
                }
                """,
                "editor_bg": "#3C3836",
                "editor_fg": "#EBDBB2",
                "preview_bg": "#3C3836",
                "preview_fg": "#EBDBB2",
            },
            "one_dark": {
                "stylesheet": """
                QWidget {
                    background-color: #282C34;
                    color: #ABB2BF;
                }
                QTextEdit {
                    background-color: #3E4451;
                    color: #ABB2BF;
                }
                QTextBrowser {
                    background-color: #3E4451;
                    color: #ABB2BF;
                }
                """,
                "editor_bg": "#3E4451",
                "editor_fg": "#ABB2BF",
                "preview_bg": "#3E4451",
                "preview_fg": "#ABB2BF",
            },
            "one_light": {
                "stylesheet": """
                QWidget {
                    background-color: #FAFAFA;
                    color: #383A42;
                }
                QTextEdit {
                    background-color: #EFF0F1;
                    color: #383A42;
                }
                QTextBrowser {
                    background-color: #EFF0F1;
                    color: #383A42;
                }
                """,
                "editor_bg": "#EFF0F1",
                "editor_fg": "#383A42",
                "preview_bg": "#EFF0F1",
                "preview_fg": "#383A42",
            },
            "material_dark": {
                "stylesheet": """
                QWidget {
                    background-color: #263238;
                    color: #B2CCD6;
                }
                QTextEdit {
                    background-color: #37474F;
                    color: #B2CCD6;
                }
                QTextBrowser {
                    background-color: #37474F;
                    color: #B2CCD6;
                }
                """,
                "editor_bg": "#37474F",
                "editor_fg": "#B2CCD6",
                "preview_bg": "#37474F",
                "preview_fg": "#B2CCD6",
            },
            "material_light": {
                "stylesheet": """
                QWidget {
                    background-color: #FAFAFA;
                    color: #546E7A;
                }
                QTextEdit {
                    background-color: #ECEFF1;
                    color: #546E7A;
                }
                QTextBrowser {
                    background-color: #ECEFF1;
                    color: #546E7A;
                }
                """,
                "editor_bg": "#ECEFF1",
                "editor_fg": "#546E7A",
                "preview_bg": "#ECEFF1",
                "preview_fg": "#546E7A",
            },
            "retro": {
                "stylesheet": """
                QWidget {
                    background-color: #000000;
                    color: #00FF00;
                }
                QTextEdit {
                    background-color: #000000;
                    color: #00FF00;
                }
                QTextBrowser {
                    background-color: #000000;
                    color: #00FF00;
                }
                """,
                "editor_bg": "#000000",
                "editor_fg": "#00FF00",
                "preview_bg": "#000000",
                "preview_fg": "#00FF00",
            },
            "cyberpunk": {
                "stylesheet": """
                QWidget {
                    background-color: #1A1A1A;
                    color: #FF0099;
                }
                QTextEdit {
                    background-color: #2A2A2A;
                    color: #FF0099;
                }
                QTextBrowser {
                    background-color: #2A2A2A;
                    color: #FF0099;
                }
                """,
                "editor_bg": "#2A2A2A",
                "editor_fg": "#FF0099",
                "preview_bg": "#2A2A2A",
                "preview_fg": "#FF0099",
            },
            "ocean": {
                "stylesheet": """
                QWidget {
                    background-color: #0F1C2E;
                    color: #A8D8FF;
                }
                QTextEdit {
                    background-color: #1F2B3E;
                    color: #A8D8FF;
                }
                QTextBrowser {
                    background-color: #1F2B3E;
                    color: #A8D8FF;
                }
                """,
                "editor_bg": "#1F2B3E",
                "editor_fg": "#A8D8FF",
                "preview_bg": "#1F2B3E",
                "preview_fg": "#A8D8FF",
            },
            "forest": {
                "stylesheet": """
                QWidget {
                    background-color: #1E2E1E;
                    color: #A8FFA8;
                }
                QTextEdit {
                    background-color: #2E3E2E;
                    color: #A8FFA8;
                }
                QTextBrowser {
                    background-color: #2E3E2E;
                    color: #A8FFA8;
                }
                """,
                "editor_bg": "#2E3E2E",
                "editor_fg": "#A8FFA8",
                "preview_bg": "#2E3E2E",
                "preview_fg": "#A8FFA8",
            },
        }

        theme = themes.get(theme_name, themes["light"])
        self.setStyleSheet(theme["stylesheet"])
        self.editor.setStyleSheet(f"background-color: {theme['editor_bg']}; color: {theme['editor_fg']};")
        self.preview.setStyleSheet(f"background-color: {theme['preview_bg']}; color: {theme['preview_fg']};")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())