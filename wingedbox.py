import sys
import os

from PyQt4 import QtGui, QtCore

from widgets import Login
from widgets import Winged

class WingedBox(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('WingedBox')
        pixmap = QtGui.QPixmap(os.getcwd() + '/img/icon.png')
        self.setWindowIcon(QtGui.QIcon(pixmap))
        self.user = ''
        self.password = ''

        self._vbox = QtGui.QVBoxLayout(self)
        self._login = Login(self)
        self._vbox.addWidget(self._login)
        self._winged = Winged(self)
        self._winged.setVisible(False)
        self._vbox.addWidget(self._winged)

        #SystemTray Menu
        self._menu = QtGui.QMenu('WingedBox')
        self._myfiles = self._menu.addAction(self.style().standardIcon(QtGui.QStyle.SP_DirOpenIcon), 'Mis Archivos')
        self._myfiles.setEnabled(False)
        self._init = self._menu.addAction(self.style().standardIcon(QtGui.QStyle.SP_DialogOkButton), 'Iniciar Sesion')
        self._init.setVisible(False)
        self._close = self._menu.addAction(self.style().standardIcon(QtGui.QStyle.SP_DialogCloseButton), 'Cerrar Sesion')
        self._menu.addSeparator()
        exit = self._menu.addAction(self.style().standardIcon(QtGui.QStyle.SP_TitleBarCloseButton), 'Salir')

        #SystemTray
        self._tray = QtGui.QSystemTrayIcon(QtGui.QIcon(pixmap), self)
        self._tray.setToolTip('WingedBox')
        self._tray.setVisible(True)
        self._tray.setContextMenu(self._menu)

        #Signal -> Slot
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        self.connect(self._myfiles, QtCore.SIGNAL("triggered()"), self.show)
        self.connect(self._init, QtCore.SIGNAL("triggered()"), self.show)
        self.connect(self._close, QtCore.SIGNAL("triggered()"), self.disconnect)

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


app = QtGui.QApplication(sys.argv)
winged = WingedBox()
winged.show()
sys.exit(app.exec_())
