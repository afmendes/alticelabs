import os

from tkinter import Tk, Frame, Label, Button, Entry, StringVar
from PySide2 import QtWidgets, QtGui


class Application:
    def __init__(self, master):
        master.geometry("400x400")

        container = Frame(master)
        container.pack()

        self.myButton = Button(master, text="Click Me!", command=self.clicker)
        self.myButton.pack(pady=20)

    def clicker(self):
        print("Look at you...you clicker a button!")



class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        self.app = None
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("AlticeLabs Chair Application Build - 1.0")

        menu = QtWidgets.QMenu(parent)
        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(self.close)
        exit_.setIcon(QtGui.QIcon("placeholder.png"))

        menu.addSeparator()
        self.setContextMenu(menu)

        """menu = QtWidgets.QMenu(parent)

        open_app = menu.addAction("Open App")
        open_app.triggered.connect(self.open_app)
        open_app.setIcon(QtGui.QIcon("placeholder.png"))

        menu.addSeparator()
        self.setContextMenu(menu)"""

        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.open_app()

    def open_app(self):
        if not self.app:
            self.app = Tk()

            Application(self.app)

            self.app.mainloop()
            ...

    def close_app(self):
        ...

    def close(self):
        self.close_app()
        exit(1)
