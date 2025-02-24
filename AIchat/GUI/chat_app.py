# chat_app.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui import add_image_to_layout
from chat_logic import send_message
from utils import load_messages
from constants import log_file
from datetime import datetime

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Amadius - AI對話助手")
        
        # 初始化消息列表
        self.messages = load_messages()  # 在调用 init_ui 之前初始化 messages
        
        self.init_ui()

    def init_ui(self):
        # 创建主窗口布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 创建聊天区域和图片的水平布局
        chat_layout = QHBoxLayout()

        # 创建对话框
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFontPointSize(14)
        chat_layout.addWidget(self.chat_area)

        # 添加图片
        add_image_to_layout(chat_layout, "image.png")

        # 添加输入框和发送按钮
        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("请输入消息...")
        main_layout.addWidget(self.input_area)

        self.send_button = QPushButton("發送")
        self.send_button.clicked.connect(self.send_message)
        main_layout.addWidget(self.send_button)

        # 将聊天布局和输入框布局组合
        main_layout.addLayout(chat_layout)

        # 设置主窗口布局
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 显示对话历史
        self.display_history()

    def send_message(self):
        user_input = self.input_area.text()
        if user_input.lower() == 'exit':
            self.close()
            return

        response = send_message(self.messages, user_input)
        self.chat_area.append(f"{datetime.now().strftime('%H:%M:%S')} 用户：{user_input}")
        self.chat_area.append(f"{datetime.now().strftime('%H:%M:%S')} Amadius：{response}")
        self.input_area.clear()

    def display_history(self):
        self.chat_area.clear()
        for message in self.messages:
            timestamp = datetime.strptime(message["timestamp"], '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S")
            if message["role"] == "user":
                self.chat_area.append(f"{timestamp} 用户：{message['content']}")
            elif message["role"] == "assistant":
                self.chat_area.append(f"{timestamp} Amadius：{message['content']}")

if __name__ == "__main__":
    app = QApplication([])
    window = ChatApp()
    window.show()
    app.exec_()

