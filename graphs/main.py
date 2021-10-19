import sys


from kevin_bacon import KevinBacon

from PyQt5.QtWidgets import (
    QApplication, QDialog, QFileDialog, QMainWindow, QMessageBox
)

# from PyQt5.uic import loadUi

from main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    kevin = KevinBacon()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.actionNew.triggered.connect(self.new)
        self.actionQuit.triggered.connect(self.close)
        self.action_About.triggered.connect(self.about)
        self.runBtn.clicked.connect(self.run)

    def new(self):
        filename, _ = QFileDialog.getOpenFileName(self, caption="Select JSON with actors", filter='*.json')
        self.kevin.construct_graph(filename)

    def run(self):
        QMessageBox.warning(self, 'RUN', "RUN!!!")

    def about(self):
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())