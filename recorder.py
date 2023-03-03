# coding:utf-8
import G
from PyQt6.QtCore import QTimer, QObject
import time


class Recorder(QObject):
    S_IDLE = 1
    S_RECORDING = 2
    S_PLAYING = 3

    def __init__(self):
        super(Recorder, self).__init__()
        self.buf = OperatingData()
        self.timer = None
        self.stat = Recorder.S_IDLE
        self.start_ts = 0
        self.repeat = 0
        self.repeat_cnt = 0
        G.Signal.S_MOUSE_EVENT.connect(self.on_mouse_event)

    @property
    def time_elapsed(self):
        return time.time() - self.start_ts if self.start_ts > 0 else 0

    def on_mouse_event(self, e, x, y, args):
        self.buf.append([self.time_elapsed, e, x, y, args])

    def start_record(self):
        if not self.stat == Recorder.S_IDLE:
            return
        self.clear()
        self.start_ts = time.time()
        G.InputManager.start_listen()
        self.stat = Recorder.S_RECORDING

    def end_record(self):
        if not self.stat == Recorder.S_RECORDING:
            return
        G.InputManager.stop_listen()
        self.stat = Recorder.S_IDLE
        G.Signal.S_RECORD_STOP.emit()

    def start_play(self, data, repeat=0):
        if not self.stat == Recorder.S_IDLE:
            return
        self.repeat = repeat
        if data is not None:
            self.buf.load(data.get('record', []))
        self.buf.reset()
        self.repeat_cnt = 0
        if not self.buf.has_next:
            return
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_simulate_tick)
        self.start_ts = time.time()
        self.timer.start(0)
        self.stat = Recorder.S_PLAYING

    def stop_play(self):
        if not self.stat == Recorder.S_PLAYING:
            return
        self.timer.stop()
        self.timer = None
        self.stat = Recorder.S_IDLE
        G.Signal.S_PLAY_STOP.emit()

    def _on_simulate_tick(self):
        delta_t = self.time_elapsed
        while self.buf.has_next and self.buf.next_ts < delta_t:
            entry = self.buf.next
            G.InputManager.operate_mouse(entry[1], entry[2], entry[3], entry[4])
        if not self.buf.has_next:
            self.repeat_cnt = self.repeat_cnt + 1
            self.start_ts = time.time()
            if self.repeat > 0 and self.repeat_cnt >= self.repeat_cnt:
                self.stop_play()
            else:
                self.buf.reset()

    def clear(self):
        self.buf.data = []


class OperatingData(object):
    def __init__(self):
        self.data = []
        self._ptr = 0

    @property
    def has_next(self):
        return self._ptr < len(self.data)

    @property
    def next(self):
        if not self.has_next:
            return None
        buf = self.data[self._ptr]
        self._ptr = self._ptr + 1
        return buf

    @property
    def next_ts(self):
        return self.data[self._ptr][0] if self.has_next else None

    def reset(self):
        self._ptr = 0

    def load(self, data):
        self.reset()
        self.data = data

    def append(self, entry):
        self.data.append(entry)
