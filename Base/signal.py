# coding:utf-8
from PyQt6.QtCore import pyqtSignal, QObject


class SignalHelper(QObject):
    S_MOUSE_EVENT = pyqtSignal(int, float, float, tuple)
    S_PLAY_STOP = pyqtSignal()
    S_RECORD_STOP = pyqtSignal()
