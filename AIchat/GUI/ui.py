# ui_components.py
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def add_image_to_layout(layout, image_path):
    try:
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            raise ValueError("图片加载失败，请检查路径是否正确")

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignRight)
        layout.addSpacing(24)
        layout.addWidget(image_label)
    except Exception as e:
        QMessageBox.critical(None, "加载图片失败", f"加载图片时出错：{e}")
