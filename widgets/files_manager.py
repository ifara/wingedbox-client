from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QColor
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

import config

class FilesUIManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._vbox = QVBoxLayout(self)
        self._hbox = QHBoxLayout()
        self._table = QTableWidget(1, 3)
        self._table.setHorizontalHeaderLabels(['Permiso', 'Archivo', 'Size'])
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.removeRow(0)
        self._table.setColumnWidth(0, 80)
        self._table.setColumnWidth(1, 480)
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
                item = QTableWidgetItem(file['name'])
            else:
                item = QTableWidgetItem(file['file-name'])
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self._table.setItem(r, 1, item)
            item = QTableWidgetItem(str(file['file-size'] / 1024) + ' kb')
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self._table.setItem(r, 2, item)
            imageFile = config.type.get(file['type'], config.typeBlank)
            access = config.access[file['accesibility']]
            item = QTableWidgetItem(QIcon(imageFile), access[3])
            item.setBackgroundColor(QColor(access[0], access[1], access[2]))
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self._table.setItem(r, 0, item)
            r += 1
        self.connect(self._btnDownload, SIGNAL("clicked()"), self._save)
        self.connect(self._btnFacebook, SIGNAL("clicked()"), self._facebook)
        self.connect(self._btnTwitter, SIGNAL("clicked()"), self._twitter)
        self._table.resizeRowsToContents()
        self._table.resizeColumnsToContents()
        self._table.horizontalHeader().setStretchLastSection(True)


class MyFiles(FilesUIManager):

    def __init__(self, winged):
        FilesUIManager.__init__(self)
        self._winged = winged
        self._btnDownload = QPushButton(QIcon(config.images['download']), '')
        btnDelete = QPushButton(QIcon(config.images['delete']), '')
        self._btnFacebook = QPushButton(QIcon(config.images['facebook']), '')
        self._btnTwitter = QPushButton(QIcon(config.images['twitter']), '')
        btnPreview = QPushButton(QIcon(config.images['preview']), '')
        btnDelete.setEnabled(False)
        btnPreview.setEnabled(False)
        vbox2 = QVBoxLayout()
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
        self._btnDownload = QPushButton(QIcon(config.images['download']), '')
        self._btnFacebook = QPushButton(QIcon(config.images['facebook']), '')
        self._btnTwitter = QPushButton(QIcon(config.images['twitter']), '')
        btnPreview = QPushButton(QIcon(config.images['preview']), '')
        btnPreview.setEnabled(False)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self._btnDownload)
        vbox2.addWidget(self._btnFacebook)
        vbox2.addWidget(self._btnTwitter)
        vbox2.addWidget(btnPreview)
        self._hbox.addLayout(vbox2)
        self._vbox.addLayout(self._hbox)