from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QColor
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

import config

class FilesUIManager(QWidget):

    def __init__(self, winged, pref):
        QWidget.__init__(self)
        self.winged = winged
        self.pref = pref
        self._vbox = QVBoxLayout(self)
        self._hbox = QHBoxLayout()
        self._table = QTableWidget(1, 3)
        self._table.setHorizontalHeaderLabels(['Access', 'File Name', 'Size'])
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.verticalHeader().hide()
        self._table.removeRow(0)
        self._table.setColumnWidth(0, 80)
        self._table.setColumnWidth(1, 480)
        self._hbox.addWidget(self._table)

        self._btnDownload = QPushButton(QIcon(config.images['download']), '')
        self._btnDownload.setToolTip('Download')
        self._btnFacebook = QPushButton(QIcon(config.images['facebook']), '')
        self._btnFacebook.setToolTip('Share on Facebook')
        self._btnTwitter = QPushButton(QIcon(config.images['twitter']), '')
        self._btnTwitter.setToolTip('Share on Twitter')
        self._btnLink = QPushButton(QIcon(config.images['link']), '')
        self._btnLink.setToolTip('Copy Link')
        self.connect(self._btnDownload, SIGNAL("clicked()"), self._save)
        self.connect(self._btnFacebook, SIGNAL("clicked()"), self._facebook)
        self.connect(self._btnTwitter, SIGNAL("clicked()"), self._twitter)
        self.connect(self._btnLink, SIGNAL("clicked()"), self._copy_link)

    def _save(self):
        file_ = self._files[self._table.currentRow()]
        if file_['accesibility'] == '2':
            if self.pref.get('ask', True):
                folderName = str(QFileDialog.getExistingDirectory(self, 'Save File in...'))
            else:
                folderName = self.pref.get('folder', '')
            if folderName != '':
                self.winged.save_file(file_, folderName)
        else:
            QMessageBox.information(self, 'Download Fail', 'You can only download public files\nwith WingedBox-Client.')

    def _facebook(self):
        file_ = self._files[self._table.currentRow()]
        self.winged.thread.api.facebook(file_)

    def _twitter(self):
        file_ = self._files[self._table.currentRow()]
        self.winged.thread.api.twitter(file_)

    def _copy_link(self):
        clipboard = QApplication.clipboard()
        file = self._files[self._table.currentRow()]
        clipboard.setText('http://wingedbox.com/downloads/' + file['id'] + "-" + file['file-name'])

    def find(self, text):
        items = self._table.findItems(text, Qt.MatchContains)
        rows = [i.row() for i in items]
        rowsCount = range(self._table.rowCount())
        rowsCount.reverse()
        for i in rowsCount:
            if i not in rows:
                self._table.removeRow(i)

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
        self._table.resizeRowsToContents()
        self._table.resizeColumnsToContents()
        self._table.horizontalHeader().setStretchLastSection(True)


class MyFiles(FilesUIManager):

    def __init__(self, winged, pref):
        FilesUIManager.__init__(self, winged, pref)
        btnDelete = QPushButton(QIcon(config.images['delete']), '')
        btnDelete.setToolTip('Delete File')
        self.btnPreview = QPushButton(QIcon(config.images['preview']), '')
        self.btnPreview.setToolTip('Preview')
        self.btnPreview.setEnabled(False)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self._btnDownload)
        vbox2.addWidget(btnDelete)
        vbox2.addWidget(self._btnFacebook)
        vbox2.addWidget(self._btnTwitter)
        vbox2.addWidget(self.btnPreview)
        vbox2.addWidget(self._btnLink)
        self._hbox.addLayout(vbox2)
        self._vbox.addLayout(self._hbox)

        self.connect(self.btnPreview, SIGNAL("clicked()"), self.preview)
        self.connect(btnDelete, SIGNAL("clicked()"), self.delete)
        self.connect(self._table, SIGNAL("itemSelectionChanged()"), self._item_changed)

    def preview(self):
        file_ = self._files[self._table.currentRow()]
        link = 'http://wingedbox.com/downloads/' + file_['id'] + "-" + file_['file-name']
        self.winged.preview_item(link)

    def delete(self):
        file_ = self._files[self._table.currentRow()]
        if file_['accesibility'] == '2':
            self._table.removeRow(self._table.currentRow())
            self.winged.delete(file_)
        else:
            QMessageBox.information(self, 'Delete Fail', 'You can only delete public files\nfrom WingedBox-Client.')

    def _item_changed(self):
        file_ = self._files[self._table.currentRow()]
        if file_['type'] == 'image':
            self.btnPreview.setEnabled(True)
        else:
            self.btnPreview.setEnabled(False)


class FriendFiles(FilesUIManager):

    def __init__(self, winged, pref):
        FilesUIManager.__init__(self, winged, pref)
        btnPreview = QPushButton(QIcon(config.images['preview']), '')
        btnPreview.setToolTip('Preview')
        btnPreview.setEnabled(False)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self._btnDownload)
        vbox2.addWidget(self._btnFacebook)
        vbox2.addWidget(self._btnTwitter)
        vbox2.addWidget(btnPreview)
        vbox2.addWidget(self._btnLink)
        self._hbox.addLayout(vbox2)
        self._vbox.addLayout(self._hbox)


class UploadFiles(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        vbox = QVBoxLayout(self)
        self.web = QWebView()
        self.web.load(QUrl('http://wingedbox.com/upload_files'))
        vbox.addWidget(self.web)


class InviteFriends(QWidget):
    
    def __init__(self, winged):
        QWidget.__init__(self)
        self.winged = winged
        vbox = QVBoxLayout(self)
        vbox.setSpacing(50)
        vbox.addWidget(QLabel('Find Friends by Name or e-mail:'))
        self.line = QLineEdit()
        self.btnFind = QPushButton('Find')
        hbox = QHBoxLayout()
        hbox.addWidget(self.line)
        hbox.addWidget(self.btnFind)
        vbox.addLayout(hbox)

        self.connect(self.btnFind, SIGNAL("clicked()"), self.find)

    def find(self):
        self.winged.find_friend(str(self.line.text()))
        self.line.setText('')