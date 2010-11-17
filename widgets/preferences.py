from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QSpinBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTabWidget
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

import styles
import config

class Preferences(QDialog):
    
    def __init__(self, parent, pref):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setModal(True)
        self.setWindowTitle('Preferences')

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(QLabel('The changes will take effect\nafter restart WingedBox-Client'))

        self.tabs = QTabWidget()
        self.updates = Updates(pref)
        self.downloads = Downloads(pref)
        self.skin = Skin(pref)
        self.tabs.addTab(self.updates, 'Update')
        self.tabs.addTab(self.downloads, 'Download')
        self.tabs.addTab(self.skin, 'Skin')
        self.vbox.addWidget(self.tabs)

        hbox = QHBoxLayout()
        self.btnSave = QPushButton('Save')
        self.btnCancel = QPushButton('Cancel')
        hbox.addWidget(self.btnCancel)
        hbox.addWidget(self.btnSave)
        self.vbox.addLayout(hbox)

        self.connect(self.btnCancel, SIGNAL("clicked()"), self.close)
        self.connect(self.btnSave, SIGNAL("clicked()"), self.save)

    def save(self):
        properties = {}
        properties['time'] = self.updates.spin.value()
        if self.downloads.checkAsk.checkState() == Qt.Checked:
            properties['ask'] = True
        else:
            properties['ask'] = False
            properties['folder'] = str(self.downloads.lineFolder.text())
        properties['noSkin'] = True if self.skin.checkNoSkin.checkState() == Qt.Checked else False
        properties['custom'] = True if self.skin.checkCustom.checkState() == Qt.Checked else False
        if properties['custom']:
            properties['skin'] = str(self.skin.text.toPlainText())
        config.create_preferences(properties)
        self.close()


class Updates(QWidget):
    
    def __init__(self, pref):
        QWidget.__init__(self)
        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel('Set the interval for updates:'))
        self.spin = QSpinBox()
        self.spin.setRange(1, 60)
        self.spin.setSuffix(' minutes')
        self.spin.setValue(pref.get('time', 10))
        vbox.addWidget(self.spin)


class Downloads(QWidget):
    
    def __init__(self, pref):
        QWidget.__init__(self)
        vbox = QVBoxLayout(self)
        self.checkAsk = QCheckBox('Ask for every Download')
        self.checkFolder = QCheckBox('Use always the following folder:')
        vbox.addWidget(self.checkAsk)
        vbox.addWidget(self.checkFolder)
        hbox = QHBoxLayout()
        self.lineFolder = QLineEdit()
        self.lineFolder.setReadOnly(True)
        self.btnBrowse = QPushButton('Browse')
        if pref.get('ask', True):
            self.checkAsk.setCheckState(Qt.Checked)
            self.btnBrowse.setEnabled(False)
        else:
            self.checkFolder.setCheckState(Qt.Checked)
            self.lineFolder.setText(pref.get('folder', ''))
        hbox.addWidget(self.lineFolder)
        hbox.addWidget(self.btnBrowse)
        vbox.addLayout(hbox)

        self.connect(self.checkAsk, SIGNAL("stateChanged(int)"), self.use_ask)
        self.connect(self.checkFolder, SIGNAL("stateChanged(int)"), self.use_folder)
        self.connect(self.btnBrowse, SIGNAL("clicked()"), self.select_folder)

    def select_folder(self):
        folderName = str(QFileDialog.getExistingDirectory(self, 'Save File in...'))
        if folderName != '':
            self.lineFolder.setText(folderName)

    def use_ask(self, val):
        if val == 2:
            self.checkAsk.setCheckState(Qt.Checked)
            self.checkFolder.setCheckState(Qt.Unchecked)
            self.btnBrowse.setEnabled(False)
            self.lineFolder.setText('')
        else:
            self.use_folder(2)

    def use_folder(self, val):
        if val == 2:
            self.checkFolder.setCheckState(Qt.Checked)
            self.checkAsk.setCheckState(Qt.Unchecked)
            self.btnBrowse.setEnabled(True)
        else:
            self.use_ask(2)


class Skin(QWidget):
    
    def __init__(self, pref):
        QWidget.__init__(self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel('Configure the CSS (Skin) for this Application'))
        self.checkDefault = QCheckBox('Default')
        self.checkCustom = QCheckBox('Custom')
        self.checkNoSkin = QCheckBox('No Skin')
        hbox = QHBoxLayout()
        hbox.addWidget(self.checkDefault)
        hbox.addWidget(self.checkCustom)
        hbox.addWidget(self.checkNoSkin)
        vbox.addLayout(hbox)

        self.text = QPlainTextEdit()
        self.text.setEnabled(False)
        self.text.setPlainText(styles.css_styles)
        vbox.addWidget(self.text)
        if pref.get('noSkin', False):
            self.checkNoSkin.setCheckState(Qt.Checked)
        elif pref.get('custom', False):
            self.checkCustom.setCheckState(Qt.Checked)
            self.text.setEnabled(True)
            self.text.setPlainText(pref.get('skin', ''))
        else:
            self.checkDefault.setCheckState(Qt.Checked)

        self.connect(self.checkDefault, SIGNAL("stateChanged(int)"), self.use_default)
        self.connect(self.checkCustom, SIGNAL("stateChanged(int)"), self.use_custom)
        self.connect(self.checkNoSkin, SIGNAL("stateChanged(int)"), self.use_no_skin)

    def use_default(self, val):
        if val == 2:
            self.checkDefault.setCheckState(Qt.Checked)
            self.checkCustom.setCheckState(Qt.Unchecked)
            self.checkNoSkin.setCheckState(Qt.Unchecked)
            self.text.setEnabled(False)

    def use_custom(self, val):
        if val == 2:
            self.checkDefault.setCheckState(Qt.Unchecked)
            self.checkCustom.setCheckState(Qt.Checked)
            self.checkNoSkin.setCheckState(Qt.Unchecked)
            self.text.setEnabled(True)

    def use_no_skin(self, val):
        if val == 2:
            self.checkDefault.setCheckState(Qt.Unchecked)
            self.checkCustom.setCheckState(Qt.Unchecked)
            self.checkNoSkin.setCheckState(Qt.Checked)
            self.text.setEnabled(False)