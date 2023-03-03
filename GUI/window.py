# coding:utf-8
import G
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from recorder import Recorder


class MainWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.label = None
        self.label_msg = None
        self.layout = None
        self.recorder = None
        self.timer = QTimer(self)

    def on_init(self):
        self.init_ui()
        self.recorder = Recorder()
        self.on_refresh_info()
        self.timer.timeout.connect(self.on_refresh_info)
        G.Signal.S_PLAY_STOP.connect(self.on_recorder_idle)
        G.Signal.S_RECORD_STOP.connect(self.on_recorder_idle)

    def init_ui(self):
        self.layout = QGridLayout()
        self.label = QLabel("按F开始/结束录制，R开始运行，ESC退出运行")
        self.label_msg = QLabel("")
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.label_msg, 1, 0)
        self.setLayout(self.layout)

        self.setGeometry(300, 300, 450, 100)
        self.setWindowTitle('鼠标自动脚本')
        self.show()

    @property
    def msg(self):
        return self.label_msg.getText()

    @msg.setter
    def msg(self, text):
        self.label_msg.setText(str(text))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F:
            self.on_start_stop_record()
        elif event.key() == Qt.Key.Key_R:
            self.on_play()
        elif event.key() == Qt.Key.Key_Escape:
            self.on_stop_play()

    def get_time_str(self):
        delta_t = int(self.recorder.time_elapsed + 0.5)
        s = delta_t % 60
        delta_t = delta_t // 60
        m = delta_t % 60
        delta_t = delta_t // 60
        return f"{delta_t:0>2d}:{m:0>2d}:{s:0>2d}"

    def on_refresh_info(self):
        if self.recorder.stat == Recorder.S_IDLE:
            self.msg = "空闲"
        elif self.recorder.stat == Recorder.S_PLAYING:
            repeat = self.recorder.repeat
            self.msg = "第 {}/{} 次运行中:".format(self.recorder.repeat_cnt + 1, repeat if repeat > 0 else "无限") \
                       + self.get_time_str()
        elif self.recorder.stat == Recorder.S_RECORDING:
            self.msg = "录制中:" + self.get_time_str()

    def on_recorder_idle(self):
        self.timer.stop()
        self.on_refresh_info()

    def on_start_stop_record(self):
        if self.recorder.stat == Recorder.S_IDLE:
            self.recorder.start_record()
            self.on_refresh_info()
            self.timer.start(1000)
        elif self.recorder.stat == Recorder.S_RECORDING:
            self.recorder.end_record()
        else:
            return

    def on_play(self):
        self.recorder.start_play(None)
        self.on_refresh_info()
        self.timer.start(1000)

    def on_stop_play(self):
        self.recorder.stop_play()
