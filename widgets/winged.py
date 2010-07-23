from PyQt4 import QtGui, QtCore

from api import Api
import config

class Winged(QtGui.QWidget):

    def __init__(self, box):
        QtGui.QWidget.__init__(self)
        self._box = box

        vbox = QtGui.QVBoxLayout(self)
        self._tabs = QtGui.QTabWidget()
        vbox.addWidget(self._tabs)

        self._myFiles = MyFiles(self)
        self._tabs.addTab(self._myFiles, QtGui.QIcon(config.images['myfiles']), 'Mis Ficheros')
        self._friends = FriendFiles(self)
        self._tabs.addTab(self._friends, QtGui.QIcon(config.images['friends']), 'Ficheros de Amigos')

        self._status = QtGui.QStatusBar()
        self._status.addWidget(QtGui.QLabel('Loading...'))
        vbox.addWidget(self._status)

    def load_tables(self, files, friends):
        self._myFiles.load_table(files)
        self._friends.load_table(friends)
        self._status.hide()

    def clean_tables():
        pass

    def show(self):
        self._box.setFixedWidth(800)
        self._box.setFixedHeight(350)
        self._api = Api(self)
        self._api.start()
        self.setVisible(True)


class FilesUIManager(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._vbox = QtGui.QVBoxLayout(self)
        self._hbox = QtGui.QHBoxLayout()
        self._table = QtGui.QTableWidget(1, 3)
        self._table.setHorizontalHeaderLabels(['Permiso', 'Archivo', 'Size'])
        self._table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._table.removeRow(0)
        self._table.setColumnWidth(0, 80)
        self._table.setColumnWidth(1, 480)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._hbox.addWidget(self._table)

    def _save(self):
        file = self._files[self._table.currentRow()]
        self._winged._api.download_file(file['id'])

    def _facebook(self):
        file = self._files[self._table.currentRow()]
        self._winged._api.facebook(file['id'], file['name'])

    def _twitter(self):
        file = self._files[self._table.currentRow()]
        self._winged._api.twitter(file['id'], file['name'])

    def load_table(self, files):
        self._files = files
        r = 0
        for file in files:
            self._table.insertRow(r)
            if len(file['name']) > 0:
                item = QtGui.QTableWidgetItem(file['name'])
            else:
                item = QtGui.QTableWidgetItem(file['file-name'])
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self._table.setItem(r, 1, item)
            item = QtGui.QTableWidgetItem(str(file['file-size'] / 1024) + ' kb')
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self._table.setItem(r, 2, item)
            imageFile = config.type.get(file['type'], config.typeBlank)
            access = config.access[file['accesibility']]
            item = QtGui.QTableWidgetItem(QtGui.QIcon(imageFile), access[3])
            item.setBackgroundColor(QtGui.QColor(access[0], access[1], access[2]))
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self._table.setItem(r, 0, item)
            r += 1
        self.connect(self._btnDownload, QtCore.SIGNAL("clicked()"), self._save)
        self.connect(self._btnFacebook, QtCore.SIGNAL("clicked()"), self._facebook)
        self.connect(self._btnTwitter, QtCore.SIGNAL("clicked()"), self._twitter)


class MyFiles(FilesUIManager):

    def __init__(self, winged):
        FilesUIManager.__init__(self)
        self._winged = winged
        self._btnDownload = QtGui.QPushButton(QtGui.QIcon(config.images['download']), '')
        btnDelete = QtGui.QPushButton(QtGui.QIcon(config.images['delete']), '')
        self._btnFacebook = QtGui.QPushButton(QtGui.QIcon(config.images['facebook']), '')
        self._btnTwitter = QtGui.QPushButton(QtGui.QIcon(config.images['twitter']), '')
        btnPreview = QtGui.QPushButton(QtGui.QIcon(config.images['preview']), '')
        btnDelete.setEnabled(False)
        btnPreview.setEnabled(False)
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self._btnDownload)
        vbox2.addWidget(btnDelete)
        vbox2.addWidget(self._btnFacebook)
        vbox2.addWidget(self._btnTwitter)
        vbox2.addWidget(btnPreview)
        self._hbox.addLayout(vbox2)
        self._vbox.addLayout(self._hbox)


class FriendFiles(FilesUIManager):

    def __init__(self, winged):
        FilesUIManager.__init__(self)
        self._winged = winged
        self._btnDownload = QtGui.QPushButton(QtGui.QIcon(config.images['download']), '')
        self._btnFacebook = QtGui.QPushButton(QtGui.QIcon(config.images['facebook']), '')
        self._btnTwitter = QtGui.QPushButton(QtGui.QIcon(config.images['twitter']), '')
        btnPreview = QtGui.QPushButton(QtGui.QIcon(config.images['preview']), '')
        btnPreview.setEnabled(False)
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self._btnDownload)
        vbox2.addWidget(self._btnFacebook)
        vbox2.addWidget(self._btnTwitter)
        vbox2.addWidget(btnPreview)
        self._hbox.addLayout(vbox2)
        self._vbox.addLayout(self._hbox)
