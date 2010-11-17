import os
import math

from PyQt4 import QtGui, QtCore

from web import Web
from thread_winged import Thread
import config
from api import Api

class Login(QtGui.QWidget):

    def __init__(self, wing, path):
        QtGui.QWidget.__init__(self)
        self._winged = wing
        self.path = path

        try:
            self._config = open(os.path.join(self.path, 'users.cfg'), 'r')
            self._names = self._config.readlines()
            self._config.close()
        except:
            self._names = []

        vbox = QtGui.QVBoxLayout(self)
        #Icon
        pixmap = QtGui.QPixmap(config.images['logo'])
        labIcon = QtGui.QLabel('')
        labIcon.setPixmap(pixmap)
        vbox.addWidget(labIcon)
        self._labelMessage = QtGui.QLabel('<font color=#FF0000><b>Login Failed!</b></font>')
        self._labelMessage.setVisible(False)
        vbox.addWidget(self._labelMessage)
        #Login
        grid = QtGui.QGridLayout()
        labEmail = QtGui.QLabel('e-mail: ')
        labPass = QtGui.QLabel('password: ')
        self._txtEmail = QtGui.QLineEdit()
        completer = QtGui.QCompleter(sorted(self._names), self._txtEmail)
        completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self._txtEmail.setCompleter(completer)
        self._txtPass = QtGui.QLineEdit()
        self._txtPass.setEchoMode(QtGui.QLineEdit.Password)
        self._checkRemember = QtGui.QCheckBox('Remember Me')
        self._btnLogin = QtGui.QPushButton('Connect!')
        grid.addWidget(labEmail, 0, 0)
        grid.addWidget(self._txtEmail, 0, 1)
        grid.addWidget(labPass, 1, 0)
        grid.addWidget(self._txtPass, 1, 1)
        grid.addWidget(self._checkRemember, 2, 1)
        grid.addWidget(self._btnLogin, 3, 1)
        btnCreate = QtGui.QPushButton(self.style().standardIcon(QtGui.QStyle.SP_MessageBoxInformation), 'Create account...')
        btnCreate.setFlat(True)
        grid.addWidget(btnCreate, 5, 0)
        vbox.addLayout(grid)

        self.overlay = Overlay(self)
        self.overlay.hide()

        self.connect(btnCreate, QtCore.SIGNAL("clicked()"), self.open_login_web)
        self.connect(self._txtEmail, QtCore.SIGNAL("returnPressed()"), self._txtPass.setFocus)
        self.connect(self._txtEmail, QtCore.SIGNAL("editingFinished()"), self._check_remember)
        self.connect(self._txtPass, QtCore.SIGNAL("returnPressed()"), self._init_session)
        self.connect(self._btnLogin, QtCore.SIGNAL("clicked()"), self._init_session)

    def _init_session(self):
        self._labelMessage.setVisible(False)
        self._winged.user = str(self._txtEmail.text()).replace('\n', '')
        self._winged.password = str(self._txtPass.text())
        self.t = Thread(self._winged.user, self._winged.password)
        self.connect(self.t, QtCore.SIGNAL("loginSuccess()"), self.login_success)
        self.connect(self.t, QtCore.SIGNAL("loginFail()"), self.login_fail)
        self.connect(self.t, QtCore.SIGNAL("userUnknown()"), self.login_unknown)
        self.overlay.show()
        self.t.start()

    def login_success(self):
        self._winged._myfiles.setEnabled(True)
        self._winged._init.setVisible(False)
        self._winged._close.setVisible(True)
        if self._checkRemember.isChecked() and (self._winged.user + '\n') not in self._names:
            self._names.append(self._winged.user + '\n')
            self._config = open(os.path.join(self.path, 'users.cfg'), 'w')
            self._config.writelines(self._names)
        self._config.close()
        self.hide()
        self._winged._winged.show()
        self.overlay.hide()

    def login_fail(self):
        self.overlay.hide()
        self._labelMessage.setVisible(True)
        self._txtEmail.setFocus()

    def login_unknown(self):
        self.overlay.hide()
        self._labelMessage.setVisible(True)
        self.open_login_web()

    def _check_remember(self):
        if str(self._txtEmail.text()) in self._names:
            self._checkRemember.setChecked(True)

    def open_login_web(self):
        web = Web(self, 'http://wingedbox.com/register')
        web.show()

    def show(self):
        self.setVisible(True)
        self._winged.setFixedWidth(350)
        self._winged.setFixedHeight(300)

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()


class Overlay(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(255, 255, 255, 127)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        for i in xrange(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(127, 127, 127)))
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