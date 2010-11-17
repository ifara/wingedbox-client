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
from PyQt4.QtGui import QSystemTrayIcon
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence
from PyQt4.QtCore import QTimeLine
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from files_manager import MyFiles
from files_manager import FriendFiles
from files_manager import UploadFiles
from files_manager import InviteFriends
from thread_winged import Thread
from api import Api
from web import Web
from status_bar import StatusBar
import config

class Winged(QWidget):

    def __init__(self, box, pref):
        QWidget.__init__(self)
        self._box = box
        self.pref = pref

        vbox = QVBoxLayout(self)

        hbox = QHBoxLayout()
        self.btnMyFiles = QPushButton(QIcon(config.images['myfiles']), 'My Files')
        self.btnFriendFiles = QPushButton(QIcon(config.images['friends']), 'Friends Files')
        self.btnUpload = QPushButton(QIcon(config.images['upload']), 'Manage/Upload')
        self.btnFind = QPushButton(QIcon(config.images['search']), 'Find Friends')
        hbox.addWidget(self.btnMyFiles)
        hbox.addWidget(self.btnFriendFiles)
        hbox.addWidget(self.btnUpload)
        hbox.addWidget(self.btnFind)
        vbox.addLayout(hbox)

        self.stack = StackedWidget()
        self.myFiles = MyFiles(self, self.pref)
        self.stack.addWidget(self.myFiles)
        self.friendFiles = FriendFiles(self, self.pref)
        self.stack.addWidget(self.friendFiles)
        self.uploadFiles = UploadFiles()
        self.stack.addWidget(self.uploadFiles)
        self.inviteFriends = InviteFriends(self)
        self.stack.addWidget(self.inviteFriends)
        vbox.addWidget(self.stack)

        self._status = StatusBar(self)
        self._status.hide()
        vbox.addWidget(self._status)

        self.overlay = Overlay(self)
        self.overlay.show()

        self.shortFind = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        
        self.connect(self.btnMyFiles, SIGNAL("clicked()"), lambda: self.stack.setCurrentIndex(0))
        self.connect(self.btnFriendFiles, SIGNAL("clicked()"), lambda: self.stack.setCurrentIndex(1))
        self.connect(self.btnUpload, SIGNAL("clicked()"), lambda: self.stack.setCurrentIndex(2))
        self.connect(self.btnFind, SIGNAL("clicked()"), lambda: self.stack.setCurrentIndex(3))
        self.connect(self.shortFind, SIGNAL("activated()"), self._status.show_status)

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.update)
        self.timer.start(self.pref.get('time', 10) * 1000 * 60)

    def update(self):
        self.tempSizeFiles = self.sizeMyFiles
        self.tempSizeFriends = self.sizeFriendFiles
        self.thread.executable = self.thread.update_files
        self.thread.start()

    def find_friend(self, name):
        self.thread.api.invite(name)

    def files_updated(self):
        self.load_tables()
        if self.tempSizeFiles != self.sizeMyFiles or self.tempSizeFriends != self.sizeFriendFiles:
            self.show_tray_message('New Files added!')

    def find(self, text):
        widget = self.stack.currentWidget()
        widget.find(text)

    def delete(self, data):
        self.thread.api.delete_file(data)

    def preview_item(self, link):
        html = '<html><body><img src="' + link + '"/></body></html>'
        self.web = Web(self, '', html)
        self.web.show()

    def save_file(self, data, folder):
        self.myFiles._btnDownload.setEnabled(False)
        self.friendFiles._btnDownload.setEnabled(False)
        self._status.showMessage('DOWNLOADING...', 2000)
        self.thread.data = data
        self.thread.folder = folder
        self.thread.executable = self.thread.download_file
        self.thread.start()

    def load_tables(self):
        self.overlay.hide()
        self.myFiles.load_table(self.thread.api.files)
        self.friendFiles.load_table(self.thread.api.filesFriends)
        self.sizeMyFiles = len(self.thread.api.files)
        self.sizeFriendFiles = len(self.thread.api.filesFriends)
        self._status.hide()

    def clean_tables(self):
        rowsCount = range(self.myFiles._table.rowCount())
        rowsCount.reverse()
        for i in rowsCount:
            self.myFiles._table.removeRow(i)
        rowsCount = range(self.friendFiles._table.rowCount())
        rowsCount.reverse()
        for i in rowsCount:
            self.friendFiles._table.removeRow(i)

    def show(self):
        self._box.setFixedWidth(800)
        self._box.setFixedHeight(350)
        self.thread = Thread(self._box.user, self._box.password)
        self.thread.executable = self.thread.get_files
        self.connect(self.thread, SIGNAL("filesList()"), self.load_tables)
        self.connect(self.thread, SIGNAL("filesUpdated()"), self.files_updated)
        self.connect(self.thread, SIGNAL("downloadFinished(QString)"), self.download_complete)
        self.thread.start()
        self.setVisible(True)

    def download_complete(self, name):
        self.show_tray_message('DOWNLOAD COMPLETE: ' + name)
        self.myFiles._btnDownload.setEnabled(True)
        self.friendFiles._btnDownload.setEnabled(True)

    def show_tray_message(self, message):
        self._box._tray.showMessage('WingedBox', message, QSystemTrayIcon.Information, 2000)

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