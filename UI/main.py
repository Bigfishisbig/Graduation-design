import sys
from UI import list
from PyQt5.QtWidgets import QApplication, QDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    ui = list.Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
