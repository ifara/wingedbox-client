from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

import config

class StatusBar(QStatusBar):
    
    def __init__(self, winged):
        QStatusBar.__init__(self)
        self.setSizeGripEnabled(False)
        self._winged = winged

        self.line = QLineEdit(self)
        #self.line.setMinimumWidth(250)
        self.btnClose = QPushButton(self.style().standardIcon(QStyle.SP_DialogCloseButton), '')
        self.btnFind = QPushButton(QIcon(config.images['find']), '')
        self.addWidget(self.btnClose)
        self.addWidget(self.line)
        self.addWidget(self.btnFind)

        self.shortEsc = QShortcut(QKeySequence(Qt.Key_Escape), self)

        self.connect(self.btnClose, SIGNAL("clicked()"), self.hide)
        self.connect(self.btnFind, SIGNAL("clicked()"), self.find)
        self.connect(self.line, SIGNAL("returnPressed()"), self.find)
        self.connect(self, SIGNAL("messageChanged(QString)"), self.message_end)
        self.connect(self.shortEsc, SIGNAL("activated()"), self.hide_status)

    def show_status(self):
        self.show()
        self.line.setFocus()

    def hide_status(self):
        self.hide()
        self._winged.load_tables()

    def find(self):
        self._winged.find(str(self.line.text()))

    def showMessage(self, message, timeout):
        self.show()
        super(StatusBar, self).showMessage(message, timeout)

    def message_end(self, message):
        if message == '':
            self.hide()
            super(StatusBar, self).clearMessage()