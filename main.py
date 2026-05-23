from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
import random

Window.size = (480, 720)
LANE_COUNT = 4
KEY_MAP = {'f': 0, 'g': 1, 'h': 2, 'j': 3}

class Note:
    def __init__(self, lane, y):
        self.lane = lane
        self.y = y
        self.speed = 3.5

class GameWidget(Widget):
    def __init__(self,** kwargs):
        super().__init__(**kwargs)
        self.lane_w = Window.width / LANE_COUNT
        self.notes = []
        self.score = 0
        self.combo = 0
        self.judgeline_y = 80

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        self.score_label = Label(text=f"Score: {self.score}", font_size=26, pos=(20, Window.height-50))
        self.combo_label = Label(text=f"Combo: {self.combo}", font_size=22, pos=(20, Window.height-90))
        self.add_widget(self.score_label)
        self.add_widget(self.combo_label)

        Clock.schedule_interval(self.spawn_note, 0.4)
        Clock.schedule_interval(self.update_game, 1/60)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, _, keycode, text, modifiers):
        if text and text.lower() in KEY_MAP:
            self.hit_lane(KEY_MAP[text.lower()])
        return True

    def hit_lane(self, lane):
        hit = False
        for note in self.notes[:]:
            if note.lane == lane and abs(note.y - self.judgeline_y) < 70:
                self.notes.remove(note)
                self.score += 100
                self.combo += 1
                hit = True
                break
        if not hit:
            self.combo = 0
        self.score_label.text = f"Score: {self.score}"
        self.combo_label.text = f"Combo: {self.combo}"

    def spawn_note(self, dt):
        self.notes.append(Note(random.randint(0,3), Window.height))

    def update_game(self, dt):
        for note in self.notes[:]:
            note.y -= note.speed
            if note.y < 0:
                self.notes.remove(note)
                self.combo = 0

        self.canvas.clear()
        with self.canvas:
            Color(0.12, 0.12, 0.16, 1)
            Rectangle(size=Window.size)

            Color(0.3, 0.3, 0.4, 1)
            for i in range(1,4):
                x = i*self.lane_w
                Rectangle(pos=(x,0), size=(2, Window.height))

            Color(1,0.3,0.3,1)
            Rectangle(pos=(0, self.judgeline_y), size=(Window.width,4))

            Color(0, 0.9, 1, 1)
            for n in self.notes:
                x = n.lane*self.lane_w + 12
                Rectangle(pos=(x, n.y), size=(self.lane_w-24, 20))

    def on_touch_down(self, touch):
        lane = int(touch.x/self.lane_w)
        if 0<=lane<4:
            self.hit_lane(lane)

class GameApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    GameApp().run()