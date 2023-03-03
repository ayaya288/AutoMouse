# coding:utf-8
import G
import sys
from PyQt6.QtWidgets import QApplication
from GUI.window import MainWindow
from Base.signal import SignalHelper
from Base.input import InputManager


if __name__ == '__main__':
    App = QApplication(sys.argv)
    G.Window = MainWindow()
    G.Signal = SignalHelper()
    G.InputManager = InputManager()
    G.Window.on_init()
    G.InputManager.on_init()
    sys.exit(App.exec())
