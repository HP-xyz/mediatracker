__author__="dvorak"
__date__ ="$Dec 18, 2011 11:50:36 AM$"
class gui_main:
    def __init__(self):
        import sys
        app = QtGui.QApplication(sys.argv)
        MainWindow = QtGui.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    print "Hello World"
