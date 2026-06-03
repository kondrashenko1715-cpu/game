from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.label import Label
from kivy.clock import Clock
from math import sqrt
import random
class TerrariaStyleGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.block_size, self.map_width, self.map_height = 45, 128, 64
        self.player_w, self.player_h, self.iron_count, self.gold_count = 20, 56, 0, 0
        self.has_iron_pickaxe, self.has_diamond_pickaxe = False, False
        self.block_hp = [[0 for _ in range(128)] for _ in range(64)]
        self.world_map = []
        for y in range(64):
            row = []
            for x in range(128):
                t = 0
                if y > 34: t = 0
                elif y == 34: t = 1
                elif 20 <= y < 34: t = 2
                else:
                    rand = random.random()
                    t = 5 if rand < 0.04 else (4 if rand < 0.12 else 3)
                row.append(t)
                if t == 3 or t == 4 or t == 5: self.block_hp[y][x] = 3
                elif t == 2: self.block_hp[y][x] = 2
                elif t == 1: self.block_hp[y][x] = 1
            self.world_map.append(row)
        self.player_x, self.player_y = 64*45, 36*45
        self.velocity_x, self.velocity_y, self.is_on_ground = 0.0, 0.0, False
        self.joy_cx, self.joy_cy, self.joy_radius, self.joy_x, self.joy_y, self.is_touching_joy = 250, 250, 140, 250, 250, False
        self.ui_text = Label(text="", font_size=22, bold=True, color=(0, 0, 0, 1))
        Clock.schedule_interval(self.update, 1.0 / 60.0)
    def is_colliding(self, nx, ny):
        for px, py in [(nx-10, ny+2), (nx+9, ny+2), (nx-10, ny+54), (nx+9, ny+54), (nx-10, ny+28), (nx+9, ny+28)]:
            bx, by = int(px // 45), int(py // 45)
            if 0 <= bx < 128 and 0 <= by < 64 and self.world_map[by][bx] > 0: return True
        return False
    def update(self, dt):
        self.canvas.clear()
        if self.is_touching_joy and self.velocity_x != 0:
            sx = 1.0 if self.velocity_x > 0 else -1.0
            for _ in range(int(abs(self.velocity_x))):
                if not self.is_colliding(self.player_x + sx, self.player_y): self.player_x += sx
                else: self.velocity_x = 0.0; break
        self.velocity_y -= 0.7
        sy = 1.0 if self.velocity_y > 0 else -1.0
        self.is_on_ground = False
        for _ in range(int(abs(self.velocity_y))):
            if not self.is_colliding(self.player_x, self.player_y + sy): self.player_y += sy
            else:
                if self.velocity_y < 0: self.is_on_ground = True
                self.velocity_y = 0.0; break
        if self.player_y < 0: self.player_x, self.player_y, self.velocity_y = 64*45, 36*45, 0
        self.player_x = max(20, min(127*45, self.player_x))
        self.cam_x, self.cam_y = self.width / 2 - self.player_x, self.height / 2 - self.player_y
        if self.has_diamond_pickaxe: self.ui_text.text = "КИРКА: АЛМАЗНАЯ (1 клик!)"
        elif self.has_iron_pickaxe: self.ui_text.text = f"Железо: 15/15 | Золото: {self.gold_count} / 20"
        else: self.ui_text.text = f"Железо: {self.iron_count} / 15 | Золото: 0 (Нужна кирка!)"
        self.ui_text.texture_update()
        with self.canvas:
            Color(0.5, 0.7, 0.9, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.height))
            for y in range(max(0, int(-self.cam_y//45)), min(64, int((-self.cam_y+self.height)//45)+1)):
                for x in range(max(0, int(-self.cam_x//45)), min(128, int((-self.cam_x+self.width)//45)+1)):
                    t = self.world_map[y][x]
                    if t > 0:
                        if t == 1: Color(0.2, 0.7, 0.2, 1)
                        elif t == 2: Color(0.55, 0.35, 0.2, 1)
                        elif t == 3: Color(0.5, 0.5, 0.5, 1)
                        elif t == 4: Color(0.8, 0.4, 0.2, 1)
                        elif t == 5: Color(0.9, 0.8, 0.1, 1)
                        hp = self.block_hp[y][x]
                        if hp == 2 and (t == 3 or t == 4 or t == 5): Color(0.35, 0.35, 0.35, 1)
                        elif hp == 1 and (t == 3 or t == 4 or t == 5): Color(0.2, 0.2, 0.2, 1)
                        elif hp == 1 and t == 2: Color(0.35, 0.2, 0.1, 1)
                        Rectangle(pos=(self.cam_x + x*45, self.cam_y + y*45), size=(44, 44))
            cx, cy = self.width / 2, self.height / 2
            Color(0.2, 0.3, 0.7, 1); Rectangle(pos=(cx - 10, cy), size=(20, 20))
            Color(0.3, 0.6, 0.3, 1); Rectangle(pos=(cx - 10, cy + 20), size=(20, 22))
            Color(0.9, 0.75, 0.65, 1); Rectangle(pos=(cx - 8, cy + 42), size=(16, 16))
            Color(0.85, 0.7, 0.4, 1); Rectangle(pos=(cx - 8, cy + 54), size=(16, 6))
            if self.has_diamond_pickaxe: Color(0.2, 0.9, 0.9, 1)
            elif self.has_iron_pickaxe: Color(0.8, 0.4, 0.2, 1)
            else: Color(0.6, 0.6, 0.6, 1)
            Line(points=[cx + 5, cy + 20, cx + 18, cy + 5], width=3)
            Color(0.2, 0.2, 0.2, 0.4); Line(circle=(250, 250, 140), width=5)
            Color(0.1, 0.6, 0.1, 0.7); Line(circle=(self.joy_x, self.joy_y, 40), width=15)
            Color(0.1, 0.5, 0.8, 0.5); Rectangle(pos=(self.width - 160, 110), size=(110, 110))
            Color(0.8, 0.8, 0.8, 0.8); Line(rect=(self.width - 160, 110, 110, 110), width=3)
            Color(1, 1, 1, 1)
            tw, th = self.ui_text.texture_size
            Rectangle(texture=self.ui_text.texture, pos=(self.width/2 - tw/2, self.height - th - 20), size=(tw, th))
    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        dist = sqrt((x - 250)**2 + (y - 250)**2)
        if dist <= 190: self.is_touching_joy = True; self.update_joystick_logic(touch)
        elif (self.width - 160) <= x <= (self.width - 50) and 110 <= y <= 220:
            if self.is_on_ground: self.velocity_y = 15.5; self.is_on_ground = False
        else:
            click_x_block = int((x - self.cam_x) // 45)
            click_y_block = int((y - self.cam_y) // 45)
            if 0 <= click_x_block < 128 and 0 <= click_y_block < 64:
                player_block_x = self.player_x / 45
                player_block_y = (self.player_y + 28) / 45
                distance_to_block = sqrt((click_x_block - player_block_x)**2 + (click_y_block - player_block_y)**2)
                if distance_to_block <= 5.0:
                    t = self.world_map[click_y_block][click_x_block]
                    if t > 0:
                        if t == 5 and not self.has_iron_pickaxe and not self.has_diamond_pickaxe: return
                        damage = self.block_hp[click_y_block][click_x_block] if self.has_diamond_pickaxe else 1
                        self.block_hp[click_y_block][click_x_block] -= damage
                        if self.block_hp[click_y_block][click_x_block] <= 0:
                            if t == 4 and not self.has_iron_pickaxe:
                                self.iron_count += 1
                                if self.iron_count >= 15: self.has_iron_pickaxe = True
                            elif t == 5:
                                self.gold_count += 1
                                if self.gold_count >= 20: self.has_diamond_pickaxe = True
                            self.world_map[click_y_block][click_x_block] = 0
    def on_touch_move(self, touch):
        if self.is_touching_joy and touch.x < self.width / 2: self.update_joystick_logic(touch)
    def on_touch_up(self, touch):
        if touch.x < self.width / 2: self.is_touching_joy = False; self.joy_x, self.joy_y, self.velocity_x = 250, 250, 0.0
    def update_joystick_logic(self, touch):
        dx = touch.x - 250
        dist = sqrt(dx*dx + (touch.y - 250)**2)
        if dist > 140: dx = (dx / dist) * 140
        self.joy_x = 250 + dx
        self.velocity_x = (dx / 140) * 5.5
class MinecraftMobileApp(App):
    def build(self): return TerrariaStyleGame()
if __name__ == "__main__":
    MinecraftMobileApp().run()
