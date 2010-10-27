import os

from PyQt4 import QtGui, QtCore

from web import Web
import config
import api

class Login(QtGui.QWidget):

    def __init__(self, wing):
        QtGui.QWidget.__init__(self)
        self._winged = wing

        if not os.path.isdir(config.users):
            os.makedirs(config.users)
        try:
            self._config = open(config.users + 'users.cfg', 'r')
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
        self._checkRemember = QtGui.QCheckBox('Recordarme')
        self._btnLogin = QtGui.QPushButton('Entrar')
        grid.addWidget(labEmail, 0, 0)
        grid.addWidget(self._txtEmail, 0, 1)
        grid.addWidget(labPass, 1, 0)
        grid.addWidget(self._txtPass, 1, 1)
        grid.addWidget(self._checkRemember, 2, 1)
        grid.addWidget(self._btnLogin, 3, 1)
        btnCreate = QtGui.QPushButton(self.style().standardIcon(QtGui.QStyle.SP_MessageBoxInformation), 'Crear Cuenta...')
        btnCreate.setFlat(True)
        grid.addWidget(btnCreate, 5, 0)
        vbox.addLayout(grid)

        self.connect(btnCreate, QtCore.SIGNAL("clicked()"), self.open_login_web)
        self.connect(self._txtEmail, QtCore.SIGNAL("returnPressed()"), self._txtPass.setFocus)
        self.connect(self._txtEmail, QtCore.SIGNAL("editingFinished()"), self._check_remember)
        self.connect(self._txtPass, QtCore.SIGNAL("returnPressed()"), self._init_session)
        self.connect(self._btnLogin, QtCore.SIGNAL("clicked()"), self._init_session)

    def _init_session(self):
        self._labelMessage.setVisible(False)
        self._winged.user = str(self._txtEmail.text()).replace('\n', '')
        self._winged.password = str(self._txtPass.text())
        bot = api.Api(self._winged.user, self._winged.password)
        auth = bot.login()
        if auth == 0:
            self._winged._myfiles.setEnabled(True)
            self._winged._init.setVisible(False)
            self._winged._close.setVisible(True)
            if self._checkRemember.isChecked():
                self._names.append(self._winged.user + '\n')
                self._config = open(config.users + 'users.cfg', 'w')
                self._config.writelines(self._names)
            self._config.close()
            self.hide()
            self._winged._winged.show()
        elif auth == 1:
            self._labelMessage.setVisible(True)
            self._txtEmail.setFocus()
        else:
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
