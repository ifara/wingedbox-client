from PyQt4 import QtCore, QtGui, QtWebKit

class Web(QtGui.QDialog):

    def __init__(self, parent, url):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle('Register a New User')
        self.setFixedWidth(1000)
        v = QtGui.QVBoxLayout(self)
        self._web = QtWebKit.QWebView()
        v.addWidget(self._web)
        #Status Bar
        self._status = QtGui.QStatusBar()
        self._prog = QtGui.QProgressBar()
        self._load = QtGui.QLabel('Loading...')
        self._status.addWidget(self._load)
        self._status.addWidget(self._prog)
        v.addWidget(self._status)

        self.connect(self._web, QtCore.SIGNAL("loadFinished(bool)"), self._status.hide)
        self.connect(self._web, QtCore.SIGNAL("loadProgress(int)"), self._progress)
        self.connect(self._web, QtCore.SIGNAL("loadStarted()"), self._status.show)
        if url != '':
            self._web.load(QtCore.QUrl(url))

    def _progress(self, porc):
        self._prog.setValue(porc)

    def closeEvent(self, event):
        event.ignore()
        self.done(0)
