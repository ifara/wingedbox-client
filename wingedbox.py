import sys
import os

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QSystemTrayIcon
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import SIGNAL

from widgets import Login
from widgets import Winged
from widgets import styles
import config

class WingedBox(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('WingedBox')
        pixmap = QPixmap(config.images['icon'])
        self.setWindowIcon(QIcon(pixmap))

        self.user = ''
        self.password = ''

        self._vbox = QVBoxLayout(self)
        self._login = Login(self)
        self._vbox.addWidget(self._login)
        self._winged = Winged(self)
        self._winged.setVisible(False)
        self._vbox.addWidget(self._winged)

        #SystemTray Menu
        self._menu = QMenu('WingedBox')
        self._myfiles = self._menu.addAction(self.style().standardIcon(QStyle.SP_DirOpenIcon), 'Mis Archivos')
        self._myfiles.setEnabled(False)
        self._init = self._menu.addAction(self.style().standardIcon(QStyle.SP_DialogOkButton), 'Iniciar Sesion')
        self._close = self._menu.addAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), 'Cerrar Sesion')
        self._close.setVisible(False)
        self._menu.addSeparator()
        exit = self._menu.addAction(self.style().standardIcon(QStyle.SP_TitleBarCloseButton), 'Salir')

        #SystemTray
        self._tray = QSystemTrayIcon(QIcon(pixmap), self)
        self._tray.setToolTip('WingedBox')
        self._tray.setVisible(True)
        self._tray.setContextMenu(self._menu)

        #Signal -> Slot
        self.connect(exit, SIGNAL("triggered()"), sys.exit)
        self.connect(self._myfiles, SIGNAL("triggered()"), self.show)
        self.connect(self._init, SIGNAL("triggered()"), self.show)
        self.connect(self._close, SIGNAL("triggered()"), self.disconnect)

    def disconnect(self):
        self.user = ''
        self.password = ''
        self._myfiles.setEnabled(False)
        self._init.setVisible(True)
        self._close.setVisible(False)
        self._winged.hide()
        self._login.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


app = QApplication(sys.argv)
styles.apply(app)
winged = WingedBox()
winged.show()
sys.exit(app.exec_())
