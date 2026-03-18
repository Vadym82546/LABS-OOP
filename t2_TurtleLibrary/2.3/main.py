import turtle
import random

# Класи компонентів

class Petal:
    def __init__(self, color, radius, angle):
        self.color = color
        self.radius = radius
        self.angle = angle

    def draw(self, t):
        t.color(self.color)
        t.begin_fill()
        for _ in range(2):
            t.circle(self.radius, self.angle)
            t.left(180 - self.angle)
        t.end_fill()

class Leaf:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def draw(self, t):
        t.color(self.color)
        t.begin_fill()
        for _ in range(2):
            t.circle(self.size, 90)
            t.left(90)
        t.end_fill()

class Stem:
    def __init__(self, color="darkgreen", thickness=4):
        self.color = color
        self.thickness = thickness

    def draw(self, t, start_x, start_y, base_x, base_y):
        t.penup()
        t.goto(start_x, start_y)
        t.pendown()
        t.color(self.color)
        t.pensize(self.thickness)
        t.goto(base_x, base_y)
        t.pensize(1) 

# Головний клас композиції

class Flower:
    def __init__(self, x, y, petal_color, num_petals=8, size=100):
        self.x = x
        self.y = y
        self.num_petals = num_petals
        self.size = size
        
        self.petal = Petal(petal_color, size, 60)
        self.stem = Stem()
        self.leaf = Leaf("green", size * 0.6)

    def draw(self, t, base_x, base_y):
        # Малюємо стебло
        self.stem.draw(t, self.x, self.y, base_x, base_y)
        
        # Малюємо листок
        mid_x = (self.x + base_x) / 2
        mid_y = (self.y + base_y) / 2
        t.penup()
        t.goto(mid_x, mid_y)
        t.setheading(random.choice([30, 150])) 
        t.pendown()
        self.leaf.draw(t)

        # Малюємо пелюстки
        t.penup()
        t.goto(self.x, self.y)
        t.setheading(0)
        t.pendown()
        
        for _ in range(self.num_petals):
            self.petal.draw(t)
            t.left(360 / self.num_petals)

        # Малюємо серединку
        t.penup()
        t.goto(self.x, self.y - self.size * 0.15)
        t.setheading(0)
        t.pendown()
        t.color("yellow", "gold")
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

    base_x, base_y = 0, -250 

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
        
        bouquet.append(Flower(x, y, color, num_petals, size))

    # Малюємо всі згенеровані квіти
    for flower in bouquet:
        flower.draw(t, base_x, base_y)

    screen.exitonclick()

if __name__ == "__main__":
    draw_random_bouquet()