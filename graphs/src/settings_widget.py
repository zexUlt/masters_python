from PyQt5.QtWidgets import QDialog

from generated.settings_ui import Ui_settingsWindow


class SettingsWidget(QDialog, Ui_settingsWindow):
    def __init__(self, parent=None, comm=None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self.comm = comm
        self.connectSignalSlots()
    
    def connectSignalSlots(self) -> None:
        self.applyBtn.clicked.connect(self.applyClicked)
        
    def applyClicked(self):
        self.comm.settingsApplied.emit(
            (
                self.forAllRBtn.isChecked(), 
                self.forSpecRBtn.isChecked()
            )
        )
