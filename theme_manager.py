"""Theme management: light/dark/system QSS for the app and CSS for the Markdown preview."""

import darkdetect
from pygments.formatters import HtmlFormatter

DARK_QSS = """
* { font-family: "Segoe UI", system-ui, sans-serif; font-size: 13px; }
QMainWindow, QWidget { background-color: #1e1e1e; color: #cccccc; }
QFrame#HeaderBar, QFrame#SettingsBar { background-color: #252526; }
QFrame#Panel { background-color: #252526; border: 1px solid #3c3c3c; border-radius: 6px; }
QLabel { color: #cccccc; background: transparent; }
QLabel#Title { font-size: 17px; font-weight: 600; color: #ffffff; }
QLabel#Banner { background-color: #5a4a00; color: #ffe9a8; border: 1px solid #7a6500; border-radius: 4px; padding: 8px 12px; }
QPushButton { background-color: #2d2d2d; color: #cccccc; border: 1px solid #3c3c3c; border-radius: 4px; padding: 6px 12px; }
QPushButton:hover { background-color: #37373d; }
QPushButton:pressed { background-color: #094771; }
QPushButton:disabled { color: #6e6e6e; border-color: #2d2d2d; background-color: #262626; }
QPushButton#Accent { background-color: #0078d4; color: #ffffff; border: none; font-weight: 600; }
QPushButton#Accent:hover { background-color: #1a86d9; }
QPushButton#Accent:disabled { background-color: #3c3c3c; color: #6e6e6e; }
QPushButton#IconButton { padding: 4px 8px; font-size: 16px; min-width: 20px; }
QComboBox { background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 4px; padding: 5px 8px; min-height: 18px; }
QComboBox:hover { border-color: #0078d4; }
QComboBox::drop-down { border: none; width: 18px; }
QComboBox QAbstractItemView { background-color: #252526; color: #cccccc; border: 1px solid #3c3c3c; selection-background-color: #094771; outline: none; }
QLineEdit { background-color: #1e1e1e; border: 1px solid #3c3c3c; border-radius: 4px; padding: 7px 9px; color: #cccccc; selection-background-color: #094771; }
QLineEdit:focus { border-color: #0078d4; }
QListWidget { background-color: #252526; border: none; outline: none; }
QListWidget::item { margin: 2px 4px; }
QListWidget::item:selected { background-color: #094771; border-radius: 4px; }
QListWidget::item:hover { background-color: #2a2d2e; border-radius: 4px; }
QPlainTextEdit { background-color: #1e1e1e; border: none; color: #d4d4d4; font-family: Consolas, "Cascadia Mono", monospace; font-size: 13px; selection-background-color: #094771; }
QProgressBar { background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 4px; text-align: center; color: #cccccc; height: 18px; }
QProgressBar::chunk { background-color: #0078d4; border-radius: 3px; }
QCheckBox { spacing: 7px; color: #cccccc; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 3px; border: 1px solid #3c3c3c; background: #2d2d2d; }
QCheckBox::indicator:checked { background-color: #0078d4; border-color: #0078d4; }
QSplitter::handle { background-color: #1e1e1e; }
QSplitter::handle:horizontal { width: 6px; }
QStatusBar { background-color: #007acc; color: #ffffff; }
QStatusBar QLabel { color: #ffffff; }
QScrollBar:vertical { background: transparent; width: 12px; margin: 0; }
QScrollBar::handle:vertical { background: #3c3c3c; border-radius: 6px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #4e4e4e; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 12px; margin: 0; }
QScrollBar::handle:horizontal { background: #3c3c3c; border-radius: 6px; min-width: 24px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QToolTip { background-color: #252526; color: #cccccc; border: 1px solid #3c3c3c; padding: 4px; }
"""

LIGHT_QSS = """
* { font-family: "Segoe UI", system-ui, sans-serif; font-size: 13px; }
QMainWindow, QWidget { background-color: #f3f3f3; color: #1e1e1e; }
QFrame#HeaderBar, QFrame#SettingsBar { background-color: #ffffff; }
QFrame#Panel { background-color: #ffffff; border: 1px solid #d4d4d4; border-radius: 6px; }
QLabel { color: #1e1e1e; background: transparent; }
QLabel#Title { font-size: 17px; font-weight: 600; color: #1e1e1e; }
QLabel#Banner { background-color: #fff4ce; color: #6a5800; border: 1px solid #e6c200; border-radius: 4px; padding: 8px 12px; }
QPushButton { background-color: #ffffff; color: #1e1e1e; border: 1px solid #d4d4d4; border-radius: 4px; padding: 6px 12px; }
QPushButton:hover { background-color: #e9e9e9; }
QPushButton:pressed { background-color: #cce5ff; }
QPushButton:disabled { color: #a0a0a0; border-color: #e4e4e4; background-color: #f5f5f5; }
QPushButton#Accent { background-color: #0078d4; color: #ffffff; border: none; font-weight: 600; }
QPushButton#Accent:hover { background-color: #1a86d9; }
QPushButton#Accent:disabled { background-color: #c8c8c8; color: #ffffff; }
QPushButton#IconButton { padding: 4px 8px; font-size: 16px; min-width: 20px; }
QComboBox { background-color: #ffffff; border: 1px solid #d4d4d4; border-radius: 4px; padding: 5px 8px; min-height: 18px; }
QComboBox:hover { border-color: #0078d4; }
QComboBox::drop-down { border: none; width: 18px; }
QComboBox QAbstractItemView { background-color: #ffffff; color: #1e1e1e; border: 1px solid #d4d4d4; selection-background-color: #cce5ff; outline: none; }
QLineEdit { background-color: #ffffff; border: 1px solid #d4d4d4; border-radius: 4px; padding: 7px 9px; color: #1e1e1e; selection-background-color: #cce5ff; }
QLineEdit:focus { border-color: #0078d4; }
QListWidget { background-color: #ffffff; border: none; outline: none; }
QListWidget::item { margin: 2px 4px; }
QListWidget::item:selected { background-color: #cce5ff; border-radius: 4px; }
QListWidget::item:hover { background-color: #eef2f6; border-radius: 4px; }
QPlainTextEdit { background-color: #ffffff; border: none; color: #1e1e1e; font-family: Consolas, "Cascadia Mono", monospace; font-size: 13px; selection-background-color: #cce5ff; }
QProgressBar { background-color: #e4e4e4; border: 1px solid #d4d4d4; border-radius: 4px; text-align: center; color: #1e1e1e; height: 18px; }
QProgressBar::chunk { background-color: #0078d4; border-radius: 3px; }
QCheckBox { spacing: 7px; color: #1e1e1e; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 3px; border: 1px solid #b0b0b0; background: #ffffff; }
QCheckBox::indicator:checked { background-color: #0078d4; border-color: #0078d4; }
QSplitter::handle { background-color: #f3f3f3; }
QSplitter::handle:horizontal { width: 6px; }
QStatusBar { background-color: #0078d4; color: #ffffff; }
QStatusBar QLabel { color: #ffffff; }
QScrollBar:vertical { background: transparent; width: 12px; margin: 0; }
QScrollBar::handle:vertical { background: #c4c4c4; border-radius: 6px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #a8a8a8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 12px; margin: 0; }
QScrollBar::handle:horizontal { background: #c4c4c4; border-radius: 6px; min-width: 24px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QToolTip { background-color: #ffffff; color: #1e1e1e; border: 1px solid #d4d4d4; padding: 4px; }
"""

DARK_PREVIEW_CSS = """
body { font-family: system-ui, "Segoe UI", sans-serif; color: #d4d4d4; background-color: #1e1e1e; line-height: 1.6; padding: 24px 28px; max-width: 900px; margin: 0 auto; }
h1, h2, h3, h4, h5, h6 { color: #ffffff; font-weight: 600; line-height: 1.25; margin-top: 1.4em; margin-bottom: 0.5em; }
h1 { font-size: 1.9em; border-bottom: 1px solid #3c3c3c; padding-bottom: .3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #3c3c3c; padding-bottom: .3em; }
p { margin: 0.7em 0; }
a { color: #4daafc; text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: Consolas, "Cascadia Code", monospace; background-color: #2d2d2d; color: #ce9178; padding: 2px 5px; border-radius: 4px; font-size: .9em; }
pre { background-color: #252526; border: 1px solid #3c3c3c; border-radius: 6px; padding: 14px; overflow-x: auto; }
pre code { background: transparent; color: inherit; padding: 0; }
blockquote { border-left: 3px solid #0078d4; margin: 0.8em 0; padding: 0.3em 1em; color: #a8a8a8; background-color: #252526; }
table { border-collapse: collapse; margin: 1em 0; width: 100%; }
th, td { border: 1px solid #3c3c3c; padding: 8px 12px; text-align: left; }
th { background-color: #2d2d2d; font-weight: 600; }
tr:nth-child(even) td { background-color: #252526; }
img { max-width: 100%; }
hr { border: none; border-top: 1px solid #3c3c3c; margin: 1.5em 0; }
ul, ol { padding-left: 1.6em; }
.codehilite { border: 1px solid #3c3c3c; border-radius: 6px; padding: 14px; overflow-x: auto; margin: 0.8em 0; }
.codehilite pre { margin: 0; padding: 0; background: transparent; border: none; }
"""

LIGHT_PREVIEW_CSS = """
body { font-family: system-ui, "Segoe UI", sans-serif; color: #1e1e1e; background-color: #ffffff; line-height: 1.6; padding: 24px 28px; max-width: 900px; margin: 0 auto; }
h1, h2, h3, h4, h5, h6 { color: #1a1a1a; font-weight: 600; line-height: 1.25; margin-top: 1.4em; margin-bottom: 0.5em; }
h1 { font-size: 1.9em; border-bottom: 1px solid #e1e4e8; padding-bottom: .3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #e1e4e8; padding-bottom: .3em; }
p { margin: 0.7em 0; }
a { color: #0078d4; text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: Consolas, "Cascadia Code", monospace; background-color: #f0f0f0; color: #c7254e; padding: 2px 5px; border-radius: 4px; font-size: .9em; }
pre { background-color: #f6f8fa; border: 1px solid #d4d4d4; border-radius: 6px; padding: 14px; overflow-x: auto; }
pre code { background: transparent; color: inherit; padding: 0; }
blockquote { border-left: 3px solid #0078d4; margin: 0.8em 0; padding: 0.3em 1em; color: #6a737d; background-color: #f6f8fa; }
table { border-collapse: collapse; margin: 1em 0; width: 100%; }
th, td { border: 1px solid #d4d4d4; padding: 8px 12px; text-align: left; }
th { background-color: #f0f0f0; font-weight: 600; }
tr:nth-child(even) td { background-color: #f9f9f9; }
img { max-width: 100%; }
hr { border: none; border-top: 1px solid #e1e4e8; margin: 1.5em 0; }
ul, ol { padding-left: 1.6em; }
.codehilite { border: 1px solid #d4d4d4; border-radius: 6px; padding: 14px; overflow-x: auto; margin: 0.8em 0; }
.codehilite pre { margin: 0; padding: 0; background: transparent; border: none; }
"""


class ThemeManager:
    MODES = ["light", "dark", "system"]
    ICONS = {"light": "☀️", "dark": "\U0001f319", "system": "\U0001f5a5️"}

    def __init__(self, mode="system"):
        self.mode = mode if mode in self.MODES else "system"

    def effective_theme(self):
        """Resolve the concrete theme ('light' or 'dark'), reading the OS for 'system'."""
        if self.mode == "system":
            detected = darkdetect.theme()  # "Light", "Dark", or None
            return (detected or "Light").lower()
        return self.mode

    def cycle(self):
        idx = self.MODES.index(self.mode)
        self.mode = self.MODES[(idx + 1) % len(self.MODES)]
        return self.mode

    def icon(self):
        return self.ICONS[self.mode]

    def apply(self, app):
        app.setStyleSheet(DARK_QSS if self.effective_theme() == "dark" else LIGHT_QSS)

    def preview_css(self):
        if self.effective_theme() == "dark":
            return DARK_PREVIEW_CSS + "\n" + HtmlFormatter(style="monokai").get_style_defs(".codehilite")
        return LIGHT_PREVIEW_CSS + "\n" + HtmlFormatter(style="default").get_style_defs(".codehilite")
