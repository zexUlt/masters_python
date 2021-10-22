from PyQt5.QtCore import QObject, pyqtSignal

class Communicator(QObject):
    settingsApplied = pyqtSignal(tuple)
    animationToggled = pyqtSignal(bool)