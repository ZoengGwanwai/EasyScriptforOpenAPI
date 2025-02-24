# main.py
import sys
from PyQt5.QtWidgets import QApplication
from chat_app import ChatApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
