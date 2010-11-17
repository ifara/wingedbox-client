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

try:
    from win32com.shell import shellcon, shell
    HOME_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
except ImportError: 
    HOME_PATH = os.path.expanduser("~")

HOME_WINGED_PATH = os.path.join(HOME_PATH, ".wingedbox_client")

if not os.path.isdir(HOME_WINGED_PATH):
        os.mkdir(HOME_WINGED_PATH)

from widgets import Login
from widgets import Winged
from widgets import styles
from widgets import preferences
import config

config.PREFERENCES_FOLDER = HOME_WINGED_PATH

class WingedBox(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('WingedBox')
        pixmap = QPixmap(config.images['icon'])
        self.setWindowIcon(QIcon(pixmap))

        self.user = ''
        self.password = ''

        self._vbox = QVBoxLayout(self)
        self._login = Login(self, HOME_WINGED_PATH)
        self._vbox.addWidget(self._login)
        self._winged = Winged(self, pref)
        self._winged.setVisible(False)
        self._vbox.addWidget(self._winged)

        #SystemTray Menu
        self._menu = QMenu('WingedBox')
        self._myfiles = self._menu.addAction(QIcon(config.images['icon']), 'Files')
        self._myfiles.setEnabled(False)
        self._init = self._menu.addAction(self.style().standardIcon(QStyle.SP_DialogOkButton), 'Init Session')
        self._close = self._menu.addAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), 'Close Session')
        self._close.setVisible(False)
        self._menu.addSeparator()
        self._properties = self._menu.addAction('Preferences')
        self._menu.addSeparator()
        exit = self._menu.addAction(self.style().standardIcon(QStyle.SP_TitleBarCloseButton), 'Exit')

        #SystemTray
        self._tray = QSystemTrayIcon(QIcon(pixmap), self)
        self._tray.setToolTip('WingedBox')
        self._tray.setVisible(True)
        self._tray.setContextMenu(self._menu)

        #Signal -> Slot
        self.connect(exit, SIGNAL("triggered()"), sys.exit)
        self.connect(self._myfiles, SIGNAL("triggered()"), self.show)
        self.connect(self._init, SIGNAL("triggered()"), self.show)
        self.connect(self._properties, SIGNAL("triggered()"), self.show_properties)
        self.connect(self._close, SIGNAL("triggered()"), self.disconnect)

    def show_properties(self):
        self.prop = preferences.Preferences(self, pref)
        self.prop.show()

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
pref = config.read_json()
if pref.get('custom', False):
    styles.apply_css(app, pref.get('skin', ''))
if not pref.get('noSkin', False):
    styles.apply(app)
winged = WingedBox()
winged.show()
sys.exit(app.exec_())
