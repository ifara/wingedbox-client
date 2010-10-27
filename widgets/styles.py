css_styles = """WingedBox {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #969696);
         }

        QLabel {
         border-radius: 4px;
         padding: 2px;
         color: black;
         }

        QPushButton {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #A6D0A7,
             stop: 0.5 #A1CBA2, stop: 1.0 #5F8960);
         border-radius: 10px;
         border-style: solid;
         padding: 6px;
         color: black;
         }

        QCheckBox{
            color: black;
        }

        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #FAFBFE, stop: 1 #9999FF);
        }

        QTableWidget {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
             stop: 0.5 #D8D8D8, stop: 1.0 #969696);
             color: #333333;
        }
        """

def apply(widget):
    widget.setStyleSheet(css_styles)