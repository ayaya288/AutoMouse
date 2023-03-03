# coding:utf-8
import G
import pynput.mouse as p_mouse
from Base import consts


class InputManager(object):
    def __init__(self):
        self._listener = None
        self._controller = None

    def on_init(self):
        self._controller = p_mouse.Controller()

    @property
    def mouse_pos(self):
        return self._controller.position

    @property
    def is_listen(self):
        return self._listener is not None

    @staticmethod
    def on_move(x, y):
        G.Signal.S_MOUSE_EVENT.emit(consts.M_MOVE, x, y, tuple([]))

    @staticmethod
    def on_click(x, y, button, pressed):
        button_str = 'unknown'
        if button == p_mouse.Button.left:
            button_str = 'left'
        elif button == p_mouse.Button.right:
            button_str = 'right'
        elif button == p_mouse.Button.middle:
            button_str = 'middle'
        G.Signal.S_MOUSE_EVENT.emit(consts.M_CLICK, x, y, tuple([button_str, pressed]))

    @staticmethod
    def on_scroll(x, y, dx, dy):
        G.Signal.S_MOUSE_EVENT.emit(consts.M_SCROLL, x, y, tuple([dx, dy]))

    def start_listen(self):
        if not self._listener:
            self._listener = p_mouse.Listener(
                on_move=InputManager.on_move,
                on_click=InputManager.on_click,
                on_scroll=InputManager.on_scroll)
        if self._listener.running:
            return
        self._listener.start()

    def stop_listen(self):
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _mouse_move_to(self, x, y):
        pos_now = self.mouse_pos
        dx = x - pos_now[0]
        dy = y - pos_now[1]
        self._controller.move(dx, dy)

    def operate_mouse(self, event, x, y, args):
        self._mouse_move_to(x, y)
        if event == consts.M_CLICK:
            btn_str, pressed = args[0], args[1]
            btn = getattr(p_mouse.Button, btn_str)
            if not btn:
                return
            if pressed:
                self._controller.press(btn)
            else:
                self._controller.release(btn)
        elif event == consts.M_SCROLL:
            dx, dy = args[0], args[1]
            self._controller.scroll(dx, dy)

    def __del__(self):
        self.stop_listen()
        return super(InputManager, self).__init__()
