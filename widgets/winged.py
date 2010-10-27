import math

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtCore import QTimeLine
from PyQt4.QtCore import QThread
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from files_manager import MyFiles
from files_manager import FriendFiles
from api import Api
import config

class Winged(QWidget):

    def __init__(self, box):
        QWidget.__init__(self)
        self._box = box

        vbox = QVBoxLayout(self)

        hbox = QHBoxLayout()
        self.btnMyFiles = QPushButton(QIcon(config.images['myfiles']), 'Mis Ficheros')
        self.btnFriendFiles = QPushButton(QIcon(config.images['friends']), 'Ficheros de Amigos')
        self.btnUpload = QPushButton(QIcon(config.images['upload']), 'Subir Ficheros')
        self.btnFind = QPushButton(QIcon(config.images['search']), 'Buscar Amigos')
        hbox.addWidget(self.btnMyFiles)
        hbox.addWidget(self.btnFriendFiles)
        hbox.addWidget(self.btnUpload)
        hbox.addWidget(self.btnFind)
        vbox.addLayout(hbox)

        self.stack = StackedWidget()
        self.myFiles = MyFiles(self)
        self.stack.addWidget(self.myFiles)
        self.friendFiles = FriendFiles(self)
        self.stack.addWidget(self.friendFiles)
        vbox.addWidget(self.stack)

        self._status = QStatusBar()
        self._status.addWidget(QLabel('Downloading...'))
        self._status.hide()
        vbox.addWidget(self._status)

        self.overlay = Overlay(self)
        self.overlay.show()

        self.connect(self.btnMyFiles, SIGNAL("clicked()"), lambda: self.stack.setCurrentIndex(0))
        self.connect(self.btnFriendFiles, SIGNAL("clicked()"), lambda: self.stack.setCurrentIndex(1))

    def load_tables(self):
        self.overlay.hide()
        self.myFiles.load_table(self.t.api.files)
        self.friendFiles.load_table(self.t.api.filesFriends)
        self._status.hide()

    def clean_tables(self):
        pass

    def show(self):
        self._box.setFixedWidth(800)
        self._box.setFixedHeight(350)
        self.t = Thread(self._box.user, self._box.password)
        self.connect(self.t, SIGNAL("finished()"), self.load_tables)
        self.t.start()
        self.setVisible(True)

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()


class StackedWidget(QStackedWidget):

    def __init__(self):
        QStackedWidget.__init__(self)

    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def show_display(self, index):
        self.setCurrentIndex(index)


class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(555)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


class Overlay(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in xrange(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height()/2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20)

        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(50)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()


class Thread(QThread):

    def __init__(self, user, password):
        QThread.__init__(self)
        self.api = Api(user, password)

    def run(self):
        self.api.get_files()