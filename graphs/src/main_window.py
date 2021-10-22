import re
import itertools

from PyQt5.QtCore import QAbstractAnimation, pyqtSignal, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from src.communicator import Communicator
from src.kevin_bacon import KevinBacon
from generated.main_window_ui import Ui_MainWindow
from src.settings_widget import SettingsWidget


class Window(QMainWindow, Ui_MainWindow):
    kevin = KevinBacon()

    fileLoaded = pyqtSignal(str)

    template_string_start = """<p>Path from <b>{:}</b> to <b>Kevin Bacon</b>:</p>""".format

    template_string_body = """<p><b>{:}</b> was in <i>{:} ({:})</i> with <b>{:}</b>.</p>""".format

    template_string_end = """<p><b>{:}\'s</b> Bacon number is <b>{:}</b>.</p><hr>""".format

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.comm = Communicator()
        self.connectSignalsSlots()
        self.animateAds()
        print(self.gridLayout.contentsRect())

    def connectSignalsSlots(self) -> None:
        self.actionNew.triggered.connect(self.new)
        self.actionQuit.triggered.connect(self.close)
        self.actionPreferences.triggered.connect(self.showPreferences)
        self.action_About.triggered.connect(self.about)
        self.runBtn.clicked.connect(self.run)
        self.comm.settingsApplied.connect(self.applySettings)
        self.fileLoaded.connect(self.updateDescr)
        self.comm.animationToggled.connect(self.toggleAnimation)

    def animateAds(self):
        starting_rect = QRect(-400, self.geometry().height() / 2 - 60, 300, 30)
        ending_rect = QRect(
                self.geometry().width() / 2 + 200, self.geometry().height() / 2 - 60, 
                300, 30
            )
        self.anim = QPropertyAnimation(self.ads, b"geometry", parent=self)
        self.anim.setDuration(3000)
        self.anim.setLoopCount(-1)
        self.anim.setStartValue(starting_rect)
        self.anim.setEndValue(ending_rect)
        self.anim.start()

    def toggleAnimation(self, newAnimState: bool):
        if newAnimState:
            if self.anim.state() == QAbstractAnimation.State.Paused:
                self.anim.resume()
        else:
            if self.anim.state() == QAbstractAnimation.State.Running:
                self.anim.pause()

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
        # self.sessionDescription.setText(
        #     "File name: {:}\n"
        #     "Path to directory: {:}".format(
        #         re.split(r'/|\\', loaded_file)[-1], 
        #         '/'.join(re.split(r'/|\\', loaded_file)[:-1])
        #         ) 
        # )

    def new(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(self, caption="Select JSON with actors", filter='*.json')
        
        if filename:
            self.kevin.constructGraph(filename)
            self.fileLoaded.emit(filename)

    def run(self) -> None:
        self.statusbar.showMessage("Kevin Bacon's number is calculating...", 1000)
        self.paths_to_kevin = self.kevin.calculateKBNumber()

        html_contents = ""
        for actor in self.paths_to_kevin:
            html_contents += self.template_string_start(actor)
            for actor_pair in zip(self.paths_to_kevin[actor], self.paths_to_kevin[actor][1:]):
                actors_meta = self.kevin.getFilmByActors(*actor_pair)
                html_contents += self.template_string_body(
                    actor_pair[0],
                    actors_meta[0],
                    actors_meta[1],
                    actor_pair[1]
                )
            html_contents += self.template_string_end(
                actor, len(self.paths_to_kevin[actor]) - 1
                )
        
        self.resultTextArea.setHtml(html_contents)


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
