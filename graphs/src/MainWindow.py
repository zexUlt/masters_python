import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QLabel, QMainWindow, QMessageBox

from .Communicator import Communicator
from .kevin_bacon import KevinBacon
from ..generated.main_window_ui import Ui_MainWindow
from .SettingsWidget import SettingsWidget


class Window(QMainWindow, Ui_MainWindow):
    kevin = KevinBacon()

    fileLoaded = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.comm = Communicator()
        self.connectSignalsSlots()

    def connectSignalsSlots(self) -> None:
        self.actionNew.triggered.connect(self.new)
        self.actionQuit.triggered.connect(self.close)
        self.actionPreferences.triggered.connect(self.showPreferences)
        self.action_About.triggered.connect(self.about)
        self.runBtn.clicked.connect(self.run)
        self.comm.settingsApplied.connect(self.applySettings)
        self.fileLoaded.connect(self.updateDescr)

    def showPreferences(self) -> None:
        settings_window = SettingsWidget(self, self.comm)
        settings_window.show()
        
    def applySettings(self, button_status: 'tuple[bool]') -> None:
        forAll, forSpec = button_status
        if forAll:
            # Show widget to display Bacon's number for each actor
            pass
        else:
            # Show widget for choosing special actors
            pass

    def updateDescr(self, loaded_file: str) -> None:
        self.statusbar.showMessage("Actor's data loaded!")
        self.sessionDescription.setText(
            "File name: {:}\n"
            "Path to directory: {:}".format(
                re.split(r'/|\\', loaded_file)[-1], 
                '/'.join(re.split(r'/|\\', loaded_file)[:-1])
                ) 
        )

    def new(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(self, caption="Select JSON with actors", filter='*.json')
        self.kevin.constructGraph(filename)
        self.fileLoaded.emit(filename)

    def run(self) -> None:
        self.statusbar.showMessage("Kevin Bacon's number is calculating...", 1000)
        self.paths_to_kevin = self.kevin.calculateKBNumber()
        a = QLabel(parent=self.widget)
        a.setText("Hello")
        a.show()

    def about(self) -> None:
        QMessageBox.about(
            self,
            "About Kevin Bacon's App",
            "<p>Simple app constucting path to Kevin Bacon!</p>"
            "<p>Built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>"
        )
