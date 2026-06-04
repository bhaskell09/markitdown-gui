"""Left panel: drag-and-drop file queue with per-item status badges and a spinner."""

import os

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".jpg", ".jpeg", ".png", ".gif",
    ".bmp", ".webp", ".html", ".htm", ".csv", ".json", ".xml", ".zip",
    ".epub", ".msg", ".txt", ".md",
}

_ICON_MAP = {
    ".pdf": "\U0001f4c4",
    ".docx": "\U0001f4dd",
    ".txt": "\U0001f4c3",
    ".md": "\U0001f4c3",
    ".pptx": "\U0001f4ca",
    ".xlsx": "\U0001f4ca",
    ".csv": "\U0001f4ca",
    ".json": "\U0001f9fe",
    ".xml": "\U0001f9fe",
    ".html": "\U0001f310",
    ".htm": "\U0001f310",
    ".zip": "\U0001f5dc️",
    ".epub": "\U0001f4d6",
    ".msg": "✉️",
    ".jpg": "\U0001f5bc️",
    ".jpeg": "\U0001f5bc️",
    ".png": "\U0001f5bc️",
    ".gif": "\U0001f5bc️",
    ".bmp": "\U0001f5bc️",
    ".webp": "\U0001f5bc️",
}

_SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

STATUS_COLORS = {
    "pending": "#888888",
    "converting": "#0078d4",
    "done": "#3fb950",
    "error": "#f85149",
}


def _icon_for(path):
    return _ICON_MAP.get(os.path.splitext(path)[1].lower(), "\U0001f4c4")


class FileRow(QFrame):
    """A single queue row. Emits ``clicked`` with its (stable) queue index."""

    clicked = pyqtSignal(int)

    def __init__(self, index, path):
        super().__init__()
        self.index = index
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        self.icon_label = QLabel(_icon_for(path))
        self.icon_label.setStyleSheet("font-size: 15px;")
        self.name_label = QLabel(os.path.basename(path))
        self.name_label.setToolTip(path)
        self.status_label = QLabel("●")
        self.status_label.setFixedWidth(20)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: %s; font-weight: bold;" % STATUS_COLORS["pending"])

        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label, 1)
        layout.addWidget(self.status_label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_badge(self, text, color):
        self.status_label.setText(text)
        self.status_label.setStyleSheet("color: %s; font-weight: bold;" % color)

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        super().mousePressEvent(event)


class FileQueueWidget(QWidget):
    item_selected = pyqtSignal(int)   # a "done" row was clicked
    skipped_files = pyqtSignal(int)   # count of dropped/picked unsupported files
    queue_cleared = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Panel")
        self.setAcceptDrops(True)
        self.files = []   # list of {path, status, markdown, output_path, error}
        self.rows = []    # parallel list of FileRow
        self._converting_index = None
        self._spinner_pos = 0

        self._spinner_timer = QTimer(self)
        self._spinner_timer.setInterval(100)
        self._spinner_timer.timeout.connect(self._tick_spinner)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        header = QLabel("FILE QUEUE")
        header.setStyleSheet("font-weight: 600; letter-spacing: 1px;")
        layout.addWidget(header)

        self.stack = QStackedWidget()
        self.placeholder = QLabel("Drop files here\nor click “+ Add Files”")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet(
            "color: #888888; font-size: 14px; border: 2px dashed #999999;"
            " border-radius: 8px; padding: 30px;"
        )
        self.list = QListWidget()
        self.list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.stack.addWidget(self.placeholder)  # index 0
        self.stack.addWidget(self.list)          # index 1
        layout.addWidget(self.stack, 1)

        self.add_btn = QPushButton("+ Add Files")
        self.add_btn.clicked.connect(self._open_picker)
        layout.addWidget(self.add_btn)

        self.clear_btn = QPushButton("\U0001f5d1 Clear Queue")
        self.clear_btn.clicked.connect(self.clear)
        layout.addWidget(self.clear_btn)

    # ---- drag & drop ----
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [u.toLocalFile() for u in event.mimeData().urls() if u.isLocalFile()]
        self.add_files(paths)
        event.acceptProposedAction()

    # ---- queue management ----
    def add_files(self, paths):
        added = 0
        skipped = 0
        for path in paths:
            if not path:
                continue
            if os.path.isfile(path) and os.path.splitext(path)[1].lower() in SUPPORTED_EXTENSIONS:
                self._append_file(path)
                added += 1
            else:
                skipped += 1
        if added:
            self.stack.setCurrentIndex(1)
        if skipped:
            self.skipped_files.emit(skipped)
        return added

    def _append_file(self, path):
        index = len(self.files)
        self.files.append(
            {"path": path, "status": "pending", "markdown": "", "output_path": "", "error": ""}
        )
        row = FileRow(index, path)
        row.clicked.connect(self._on_row_clicked)
        item = QListWidgetItem(self.list)
        item.setSizeHint(row.sizeHint())
        self.list.addItem(item)
        self.list.setItemWidget(item, row)
        self.rows.append(row)

    def _on_row_clicked(self, index):
        self.list.setCurrentRow(index)
        if 0 <= index < len(self.files) and self.files[index]["status"] == "done":
            self.item_selected.emit(index)

    def set_status(self, index, status, error=None):
        if not (0 <= index < len(self.files)):
            return
        self.files[index]["status"] = status
        row = self.rows[index]
        if status == "pending":
            row.set_badge("●", STATUS_COLORS["pending"])
        elif status == "converting":
            self._converting_index = index
            self._spinner_pos = 0
            row.set_badge(_SPINNER_FRAMES[0], STATUS_COLORS["converting"])
            if not self._spinner_timer.isActive():
                self._spinner_timer.start()
        elif status == "done":
            if self._converting_index == index:
                self._converting_index = None
            row.set_badge("✓", STATUS_COLORS["done"])
            self._maybe_stop_spinner()
        elif status == "error":
            self.files[index]["error"] = error or ""
            if self._converting_index == index:
                self._converting_index = None
            row.set_badge("✗", STATUS_COLORS["error"])
            row.status_label.setToolTip(error or "Conversion failed")
            self._maybe_stop_spinner()

    def _maybe_stop_spinner(self):
        if self._converting_index is None and self._spinner_timer.isActive():
            self._spinner_timer.stop()

    def _tick_spinner(self):
        if self._converting_index is None:
            self._spinner_timer.stop()
            return
        self._spinner_pos = (self._spinner_pos + 1) % len(_SPINNER_FRAMES)
        self.rows[self._converting_index].set_badge(
            _SPINNER_FRAMES[self._spinner_pos], STATUS_COLORS["converting"]
        )

    def set_result(self, index, markdown_text, output_path):
        if 0 <= index < len(self.files):
            self.files[index]["markdown"] = markdown_text
            self.files[index]["output_path"] = output_path

    def get_file(self, index):
        if 0 <= index < len(self.files):
            return self.files[index]
        return None

    def file_paths(self):
        return [f["path"] for f in self.files]

    def clear(self):
        self._spinner_timer.stop()
        self._converting_index = None
        self.list.clear()
        self.files = []
        self.rows = []
        self.stack.setCurrentIndex(0)
        self.queue_cleared.emit()

    def _open_picker(self):
        exts = " ".join("*" + e for e in sorted(SUPPORTED_EXTENSIONS))
        filter_str = f"Supported files ({exts});;All files (*)"
        paths, _ = QFileDialog.getOpenFileNames(self, "Add Files", "", filter_str)
        if paths:
            self.add_files(paths)
