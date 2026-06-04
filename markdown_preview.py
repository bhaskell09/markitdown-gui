"""Markdown preview panel: rendered (QWebEngineView) <-> raw (QPlainTextEdit) with copy/save."""

import markdown
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

MD_EXTENSIONS = ["tables", "fenced_code", "codehilite", "toc", "nl2br"]


class MarkdownPreview(QWidget):
    def __init__(self, theme_manager):
        super().__init__()
        self.setObjectName("Panel")
        self.theme_manager = theme_manager
        self._markdown_text = ""
        self._basename = "output"
        self._has_content = False
        self._raw_mode = False
        self._build_ui()
        self._update_buttons()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("HeaderBar")
        hbox = QHBoxLayout(header)
        hbox.setContentsMargins(10, 8, 10, 8)
        hbox.setSpacing(8)

        title = QLabel("PREVIEW")
        title.setStyleSheet("font-weight: 600; letter-spacing: 1px;")
        hbox.addWidget(title)
        hbox.addStretch(1)

        self.toggle_btn = QPushButton("Raw")
        self.toggle_btn.setToolTip("Toggle rendered / raw Markdown")
        self.toggle_btn.clicked.connect(self.toggle_mode)
        hbox.addWidget(self.toggle_btn)

        self.copy_btn = QPushButton("\U0001f4cb Copy")
        self.copy_btn.clicked.connect(self.copy_markdown)
        hbox.addWidget(self.copy_btn)

        self.save_btn = QPushButton("\U0001f4be Save")
        self.save_btn.clicked.connect(self.save_as)
        hbox.addWidget(self.save_btn)

        layout.addWidget(header)

        self.stack = QStackedWidget()
        self.placeholder = QLabel("Select a converted file to preview.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: #888888; font-size: 14px;")
        self.webview = QWebEngineView()
        self.raw_edit = QPlainTextEdit()
        self.raw_edit.setReadOnly(True)
        self.raw_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.stack.addWidget(self.placeholder)  # index 0
        self.stack.addWidget(self.webview)       # index 1
        self.stack.addWidget(self.raw_edit)      # index 2
        layout.addWidget(self.stack, 1)

    # ---- public API ----
    def show_markdown(self, text, basename="output"):
        self._markdown_text = text or ""
        self._basename = basename or "output"
        self._has_content = True
        self._render()
        self._update_buttons()
        self._sync_stack()

    def clear(self):
        self._markdown_text = ""
        self._has_content = False
        self.raw_edit.setPlainText("")
        self.webview.setHtml("")
        self.stack.setCurrentIndex(0)
        self._update_buttons()

    def update_theme(self):
        if self._has_content:
            self._render()

    # ---- internals ----
    def _render(self):
        md_html = markdown.markdown(self._markdown_text, extensions=MD_EXTENSIONS)
        theme_css = self.theme_manager.preview_css()
        html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<style>{theme_css}</style>
</head><body>{md_html}</body></html>"""
        self.webview.setHtml(html)
        self.raw_edit.setPlainText(self._markdown_text)

    def toggle_mode(self):
        self._raw_mode = not self._raw_mode
        self.toggle_btn.setText("Rendered" if self._raw_mode else "Raw")
        self._sync_stack()

    def _sync_stack(self):
        if not self._has_content:
            self.stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(2 if self._raw_mode else 1)

    def copy_markdown(self):
        QApplication.clipboard().setText(self._markdown_text)

    def save_as(self):
        if not self._has_content:
            return
        default_name = self._basename + ".md"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown", default_name, "Markdown (*.md);;All Files (*)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._markdown_text)

    def _update_buttons(self):
        for btn in (self.toggle_btn, self.copy_btn, self.save_btn):
            btn.setEnabled(self._has_content)
