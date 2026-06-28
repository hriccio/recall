from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from recall.app.ui.main_window import MainWindow


STYLESHEET = """
QWidget {
    background: #f4efe6;
    color: #1f2a24;
    font-family: "Noto Sans", "DejaVu Sans", sans-serif;
    font-size: 15px;
}
QLabel#Title {
    font-size: 38px;
    font-weight: 700;
    color: #18221d;
}
QLabel#Subtitle, QLabel#Muted {
    color: #66736b;
}
QLabel#Question {
    font-size: 22px;
    font-weight: 650;
}
QLabel#Excerpt {
    background: #fff9ef;
    border: 1px solid #d8cab8;
    border-radius: 10px;
    padding: 14px;
}
QLabel[correct="true"] {
    color: #225c39;
}
QLabel[correct="false"] {
    color: #8b332b;
}
QFrame#Card {
    background: #fff9ef;
    border: 1px solid #d8cab8;
    border-radius: 14px;
}
QPushButton {
    background: #e7dccb;
    border: 1px solid #cdbda7;
    border-radius: 10px;
    padding: 10px 14px;
}
QPushButton:hover {
    background: #ded0bc;
}
QPushButton#Primary {
    background: #234c3a;
    color: #fffaf1;
    border-color: #234c3a;
}
QRadioButton {
    background: #fff9ef;
    border: 1px solid #d8cab8;
    border-radius: 12px;
    padding: 12px;
}
QSpinBox {
    background: #fff9ef;
    border: 1px solid #cdbda7;
    border-radius: 8px;
    padding: 6px;
}
"""


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Recall")
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
