'''Autoclicker python kivy
'''
# -*- coding: utf-8 -*-
import threading
import time
import random
import pyautogui
import keyboard  # pip install keyboard
from pynput import mouse
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

try:
    import win32gui
except ImportError:
    win32gui = None

# Adjust window size
w, h = Window.size
Window.size = (w, int(h * 1.33))

# KV definition
KV = r'''
#:import dp kivy.metrics.dp
<Divider@Widget>:
    size_hint_y: None
    height: dp(1)
    canvas.before:
        Color:
            rgba: .6, .6, .6, 1
        Rectangle:
            size: self.size
            pos: self.pos

<RootWidget>:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(12)

    ScrollView:
        do_scroll_x: False
        bar_width: dp(8)
        GridLayout:
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(16)

            # ---------- Mode ----------
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(12)
                Label:
                    text: 'Mode:'
                    size_hint_x: None
                    width: dp(70)
                ToggleButton:
                    id: rb_fix
                    text: 'Fixed'
                    group: 'mode'
                    state: 'down'
                    on_release: root.update_mode(True)
                ToggleButton:
                    id: rb_free
                    text: 'Free'
                    group: 'mode'
                    on_release: root.update_mode(False)

            Divider:
            # ---------- Target Window ----------
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(10)
                CheckBox:
                    id: cb_use_win
                    active: True
                Label:
                    text: 'Use target window'
                    size_hint_x: None
                    width: dp(150)
                Button:
                    text: 'Set window'
                    size_hint_x: None
                    width: dp(130)
                    on_release: root.set_target_window()
            TextInput:
                id: txt_window
                text: root.target_title
                readonly: True
                size_hint_y: None
                height: dp(36)

            Divider:
            # ---------- Fixed Click Settings ----------
            BoxLayout:
                id: box_fix
                orientation: 'vertical'
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                BoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)
                    Button:
                        text: 'Set point'
                        size_hint_x: None
                        width: dp(150)
                        on_release: root.set_fixed_point()
                    TextInput:
                        id: txt_point
                        text: root.fixed_label
                        readonly: True
                BoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)
                    Label:
                        text: 'Width:'
                        size_hint_x: None
                        width: dp(80)
                    TextInput:
                        id: txt_width
                        text: str(root.box_width)
                        input_filter: 'int'
                    Label:
                        text: 'Height:'
                        size_hint_x: None
                        width: dp(80)
                    TextInput:
                        id: txt_height
                        text: str(root.box_height)
                        input_filter: 'int'

            # ---------- Free Click Settings ----------
            BoxLayout:
                id: box_free
                orientation: 'vertical'
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                BoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)
                    Button:
                        text: 'Top-left corner'
                        size_hint_x: None
                        width: dp(150)
                        on_release: root.set_top_left()
                    TextInput:
                        id: txt_tl
                        text: root.tl_label
                        readonly: True
                BoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)
                    Button:
                        text: 'Bottom-right corner'
                        size_hint_x: None
                        width: dp(150)
                        on_release: root.set_bottom_right()
                    TextInput:
                        id: txt_br
                        text: root.br_label
                        readonly: True

            Divider:
            # ---------- Delay & Counter ----------
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(16)
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(8)

                CheckBox:
                    id: cb_delay
                    active: True

                Label:
                    text: 'Delay (ms):'
                    size_hint_x: None
                    width: dp(90)

                Button:
                    text: '-'
                    size_hint_x: None
                    width: dp(40)
                    on_release: root.decrease_delay()

                TextInput:
                    id: txt_delay
                    text: str(root.click_delay)
                    input_filter: 'int'
                    size_hint_x: None
                    width: dp(80)
                    on_text_validate: root.update_delay_from_text()

                Button:
                    text: '+'
                    size_hint_x: None
                    width: dp(40)
                    on_release: root.increase_delay()

                CheckBox:
                    id: cb_show
                    active: True
                Label:
                    text: 'Counter:'
                    size_hint_x: None
                    width: dp(90)
                TextInput:
                    id: txt_total
                    text: str(root.total_clicks)
                    readonly: True
                    size_hint_x: None
                    width: dp(80)
                Button:
                    text: 'Reset'
                    size_hint_x: None
                    width: dp(60)
                    on_release: root.reset_counter()

            Divider:
            # ---------- Control Buttons ----------
            BoxLayout:
                size_hint_y: None
                height: dp(50)
                spacing: dp(30)
                padding: [dp(50), 0]
                Button:
                    text: 'Start'
                    on_release: root.start_clicker()
                Button:
                    text: 'Stop'
                    on_release: root.stop_clicker()
                Button:
                    text: 'Reset All'
                    on_release: root.reset_all()

    Divider:
    TextInput:
        id: log_area
        size_hint_y: None
        height: dp(80)
        readonly: True
        background_color: .12, .12, .12, 1
        foreground_color: 1, 1, 1, 1
        font_size: '13sp'
        cursor_width: 0
'''

# Load KV
Builder.load_string(KV)

# PyAutoGUI settings
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

class RootWidget(BoxLayout):
    # Properties
    fixed_mode = BooleanProperty(True)
    click_delay = NumericProperty(2000)
    total_clicks = NumericProperty(0)
    target_title = StringProperty('')
    target_hwnd = NumericProperty(0)
    fixed_x = NumericProperty(0)
    fixed_y = NumericProperty(0)
    box_width = NumericProperty(40)
    box_height = NumericProperty(40)
    tl_x = NumericProperty(0)
    tl_y = NumericProperty(0)
    br_x = NumericProperty(0)
    br_y = NumericProperty(0)
    stop_flag = False
    clicking_thread = None
    running = BooleanProperty(False)

    @property
    def fixed_label(self):
        return f'X={int(self.fixed_x)} Y={int(self.fixed_y)}'

    @property
    def tl_label(self):
        return f'X={int(self.tl_x)} Y={int(self.tl_y)}'

    @property
    def br_label(self):
        return f'X={int(self.br_x)} Y={int(self.br_y)}'

    def start_clicking(self):
        """Start the click loop in a background thread and bind the hotkey."""
        if self.running:
            return
        self.running = True

        # Global hotkey Esc → stop_clicking
        keyboard.add_hotkey("esc", self.stop_clicking)

        # Launch click loop
        threading.Thread(target=self._click_loop, daemon=True).start()
        self.log("Autoclicker started (Esc to stop)")

    def _click_loop(self):
        """Click loop: runs as long as running is True."""
        import pyautogui
        while self.running:
            pyautogui.click()
            threading.Event().wait(self.click_delay / 1000)

    def stop_clicking(self):
        """Stop the click loop."""
        if not self.running:
            return
        self.running = False
        self.log("Autoclicker stopped")

    def decrease_delay(self):
        """Decrease delay by 1000 ms (min 0)."""
        self.click_delay = max(self.click_delay - 1000, 0)
        self.ids.txt_delay.text = str(self.click_delay)
        self.log(f"Delay updated: {self.click_delay} ms")

    def increase_delay(self):
        """Increase delay by 1000 ms."""
        self.click_delay += 1000
        self.ids.txt_delay.text = str(self.click_delay)
        self.log(f"Delay updated: {self.click_delay} ms")

    def update_delay_from_text(self):
        """Sync click_delay when input is validated."""
        try:
            value = max(int(self.ids.txt_delay.text), 0)
            self.click_delay = value
            self.log(f"Delay updated from input: {self.click_delay} ms")
        except ValueError:
            self.log("❌ Invalid delay")

    def log(self, msg):
        """Append a message to the log area."""
        area = self.ids.log_area
        area.text += msg + '\n'
        area.cursor = (0, len(area.text.split('\n')))
        if len(area.text) > 3000:
            area.text = '\n'.join(area.text.split('\n')[-150:])

    # ---------- UI helpers ----------
    def update_mode(self, fixed):
        self.fixed_mode = fixed
        self.ids.box_fix.disabled = not fixed
        self.ids.box_free.disabled = fixed
        self.ids.box_fix.opacity = 1 if fixed else 0.25
        self.ids.box_free.opacity = 1 if not fixed else 0.25
        self.log(f"Mode ➜ {'Fixed' if fixed else 'Free'}")

    def _capture_click(self, callback):
        """Capture a single mouse click and call the given callback."""
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                listener.stop()
                Clock.schedule_once(lambda dt: callback(x, y), 0)
        self.log('🖱️  Click…')
        listener = mouse.Listener(on_click=on_click)
        listener.start()

    def set_target_window(self):
        self._capture_click(self._on_target)

    def _on_target(self, x, y):
        if win32gui:
            hwnd = win32gui.WindowFromPoint((int(x), int(y)))
            self.target_hwnd, self.target_title = hwnd, win32gui.GetWindowText(hwnd)
            self.ids.txt_window.text = self.target_title
            self.log(f'Window = {self.target_title}')
        else:
            self.log('pywin32 absent – filter inactive')

    def set_fixed_point(self):
        self._capture_click(self._upd_fixed)

    def _upd_fixed(self, x, y):
        self.fixed_x, self.fixed_y = x, y
        self.ids.txt_point.text = self.fixed_label
        self.log(f'Point {self.fixed_label}')

    def set_top_left(self):
        self._capture_click(self._upd_tl)

    def _upd_tl(self, x, y):
        self.tl_x, self.tl_y = x, y
        self.ids.txt_tl.text = self.tl_label
        self.log(f'Top-left corner {self.tl_label}')

    def set_bottom_right(self):
        self._capture_click(self._upd_br)

    def _upd_br(self, x, y):
        self.br_x, self.br_y = x, y
        self.ids.txt_br.text = self.br_label
        self.log(f'Bottom-right corner {self.br_label}')

    def reset_counter(self):
        """Reset the click counter."""
        self.total_clicks = 0
        self.ids.txt_total.text = '0'
        self.log('Counter reset to zero')

    def reset_all(self):
        """Reset all settings and stop clicking."""
        self.stop_clicking()
        self.reset_counter()
        self.fixed_x = self.fixed_y = 0
        self.tl_x = self.tl_y = self.br_x = self.br_y = 0
        self.ids.txt_point.text = self.fixed_label
        self.ids.txt_tl.text = self.tl_label
        self.ids.txt_br.text = self.br_label
        self.log('All settings reset')

    def start_clicker(self):
        """Start the clicker thread."""
        if self.clicking_thread and self.clicking_thread.is_alive():
            return
        try:
            self.click_delay = max(int(self.ids.txt_delay.text), 1)
        except ValueError:
            return self.log('❌ Invalid delay')
        self.delay_active = self.ids.cb_delay.active
        self.show_counter = self.ids.cb_show.active
        self.use_filter = self.ids.cb_use_win.active

        self.stop_flag = False
        keyboard.add_hotkey(
            "esc",
            lambda: Clock.schedule_once(lambda dt: self.stop_clicker(), 0)
        )
        self.log('▶ Clicker started')
        self.clicking_thread = threading.Thread(target=self._worker, daemon=True)
        self.clicking_thread.start()

    def stop_clicker(self):
        """Signal the worker thread to stop."""
        if self.stop_flag:
            return
        self.stop_flag = True
        self.log('■ Clicker stopped')

    def _worker(self):
        """Worker thread: perform clicks without direct UI interaction."""
        try:
            delay = self.click_delay / 1000.0 if self.delay_active else 0.001
            while not self.stop_flag:
                if self.use_filter and self.target_hwnd and win32gui:
                    if win32gui.GetForegroundWindow() != self.target_hwnd:
                        win32gui.ShowWindow(self.target_hwnd, 9)
                        win32gui.SetForegroundWindow(self.target_hwnd)
                if self.fixed_mode:
                    x, y = self.fixed_x, self.fixed_y
                else:
                    if self.br_x <= self.tl_x or self.br_y <= self.tl_y:
                        time.sleep(0.05)
                        continue
                    x = random.randint(self.tl_x, self.br_x)
                    y = random.randint(self.tl_y, self.br_y)
                pyautogui.moveTo(x, y, duration=0)
                pyautogui.click()
                Clock.schedule_once(self._after_click, 0)
                time.sleep(delay)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.log(f'❌ Thread error: {e}'), 0)

    def _after_click(self, _dt):
        """Update UI after each click."""
        self.total_clicks += 1
        if self.show_counter:
            self.ids.txt_total.text = str(self.total_clicks)
        self.log(f'Click #{self.total_clicks}')

class AutoclickerApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    AutoclickerApp().run()
