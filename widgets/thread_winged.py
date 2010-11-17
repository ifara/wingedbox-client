from PyQt4.QtCore import QThread
from PyQt4.QtCore import SIGNAL

from api import Api

class Thread(QThread):

    def __init__(self, user, password):
        QThread.__init__(self)
        self.api = Api(user, password)
        self.executable = self.login
        self.data = None
        self.folder = ''

    def run(self):
        self.executable()
        self.data = None
        self.folder = ''

    def login(self):
        auth = self.api.login()
        if auth == 0:
            self.emit(SIGNAL("loginSuccess()"))
        elif auth == 1:
            self.emit(SIGNAL("loginFail()"))
        else:
            self.emit(SIGNAL("userUnknown()"))

    def get_files(self):
        self.api.get_files()
        self.emit(SIGNAL("filesList()"))

    def update_files(self):
        self.api.get_files()
        self.emit(SIGNAL("filesUpdated()"))

    def download_file(self):
        self.api.download_file(self.data, self.folder)
        self.emit(SIGNAL("downloadFinished(QString)"), self.data['file-name'])