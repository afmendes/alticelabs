import sys

from classes.Application import *


def main():
    """app = Application()
    app.mainloop()"""
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("placeholder.png"), w)
    tray_icon.show()
    #tray_icon.showMessage("TEST1", "TEST2")
    sys.exit(app.exec_())


main()
