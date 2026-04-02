import turtle
import random

# Класи компонентів

class Petal:
    def __init__(self, color, radius, angle):
        self.color = color
        self.radius = radius
        self.angle = angle

    def draw(self, t, override_color=None):
        t.color(override_color if override_color else self.color)
        t.begin_fill()
        for _ in range(2):
            t.circle(self.radius, self.angle)
            t.left(180 - self.angle)
        t.end_fill()

class Leaf:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def draw(self, t, override_color=None):
        t.color(override_color if override_color else self.color)
        t.begin_fill()
        for _ in range(2):
            t.circle(self.size, 90)
            t.left(90)
        t.end_fill()

class Stem:
    def __init__(self, color="darkgreen", thickness=4):
        self.color = color
        self.thickness = thickness

    def draw(self, t, start_x, start_y, base_x, base_y, override_color=None):
        t.penup()
        t.goto(start_x, start_y)
        t.pendown()
        t.color(override_color if override_color else self.color)
        t.pensize(self.thickness)
        t.goto(base_x, base_y)
        t.pensize(1) 

# Головний клас композиції

class Flower:
    def __init__(self, x, y, petal_color, num_petals=8, size=100, bg_color="skyblue"):
        # a) Позиція фігури на екрані
        self.x = x 
        self.y = y
        self.base_x = 0   # Точка збору букета (для стебла)
        self.base_y = -250
        
        self.num_petals = num_petals
        self.size = size
        self.bg_color = bg_color
        
        # b) Стан: чи зображена фігура
        self.is_visible = False
        
        self.petal = Petal(petal_color, size, 60)
        self.stem = Stem()
        self.leaf = Leaf("green", size * 0.6)
        self.leaf_angle = random.choice([30, 150])

    def is_shown(self):
        return self.is_visible

    def set_color(self, color):
        # c) Встановлення кольору малювання
        self.petal.color = color

    def draw(self, t):
        # d) Зображення фігури (якщо її не зображено)
        if not self.is_visible:
            self._render(t)
            self.is_visible = True

    def erase(self, t):
        # e) Стирання фігури (якщо зображена) кольором фону
        if self.is_visible:
            self._render(t, erase=True)
            self.is_visible = False

    def move(self, t, new_x, new_y):
        # f) Переміщення фігури
        originally_visible = self.is_visible
        if originally_visible:
            self.erase(t)
        
        self.x, self.y = new_x, new_y
        
        if originally_visible:
            self.draw(t)

    def _render(self, t, erase=False):
        color_mode = self.bg_color if erase else None
        
        # Малюємо стебло
        self.stem.draw(t, self.x, self.y, self.base_x, self.base_y, color_mode)
        
        # Малюємо листок
        mid_x, mid_y = (self.x + self.base_x) / 2, (self.y + self.base_y) / 2
        t.penup()
        t.goto(mid_x, mid_y)
        t.setheading(self.leaf_angle) 
        t.pendown()
        self.leaf.draw(t, color_mode)

        # Малюємо пелюстки
        t.penup()
        t.goto(self.x, self.y)
        t.setheading(0)
        t.pendown()
        
        for _ in range(self.num_petals):
            self.petal.draw(t, color_mode)
            t.left(360 / self.num_petals)

        # Малюємо серединку
        t.penup()
        t.goto(self.x, self.y - self.size * 0.15)
        t.setheading(0)
        t.pendown()
        t.color(self.bg_color if erase else "yellow", self.bg_color if erase else "gold")
        t.begin_fill()
        t.circle(self.size * 0.15)
        t.end_fill()

# Головна функція

def draw_random_bouquet():
    screen = turtle.Screen()
    screen.bgcolor("skyblue")
    screen.title("Випадковий букет квітів")
    
    t = turtle.Turtle()
    t.speed(0) 
    t.hideturtle()

    # Можливі кольори пелюсток
    colors = ["red", "purple", "orange", "pink", "white", "crimson", "magenta", "coral", "lightpink", "gold"]
    
    # Генерація випадкової кількості квітів від 5 до 12
    num_flowers = random.randint(5, 12)
    bouquet = []

    # Створюємо квіти з випадковими параметрами
    for _ in range(num_flowers):
        x = random.randint(-220, 220)
        y = random.randint(-20, 180)
        color = random.choice(colors)
        num_petals = random.randint(5, 12)
        size = random.randint(50, 110)     
        
        bouquet.append(Flower(x, y, color, num_petals, size, bg_color="skyblue"))

    # Малюємо всі згенеровані квіти
    for flower in bouquet:
        flower.draw(t)

    screen.exitonclick()

if __name__ == "__main__":
    draw_random_bouquet()