import tkinter as tk
import random
import math

class Ball:
    """Клас, що відповідає за окрему кульку."""
    
    COLORS = ["#EC1D19", "#15DC2C", "#3915EC", "#E10ED7", "#F3FE1D", "#11ECE1", "#EA8E16"]
    RADIUS = 15

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        
        # Випадковий початковий напрямок (швидкість по x та y)
        # Виключаємо нульову швидкість, щоб кулька не стояла на місці
        speeds = [-5, -4, -3, 3, 4, 5]
        self.vx = random.choice(speeds)
        self.vy = random.choice(speeds)
        
        # Випадковий колір
        self.color = random.choice(self.COLORS)
        
        # Створення об'єкта на Canvas
        self.id = self.canvas.create_oval(
            self.x - self.RADIUS, self.y - self.RADIUS,
            self.x + self.RADIUS, self.y + self.RADIUS,
            fill=self.color, outline="black", width=2
        )

    def move(self, width, height):
        """Оновлює координати кульки та перевіряє зіткнення зі стінами."""
        self.x += self.vx
        self.y += self.vy

        # Відбивання від лівої та правої межі
        if self.x - self.RADIUS <= 0:
            self.x = self.RADIUS
            self.vx = abs(self.vx)
        elif self.x + self.RADIUS >= width:
            self.x = width - self.RADIUS
            self.vx = -abs(self.vx)

        # Відбивання від верхньої та нижньої межі
        if self.y - self.RADIUS <= 0:
            self.y = self.RADIUS
            self.vy = abs(self.vy)
        elif self.y + self.RADIUS >= height:
            self.y = height - self.RADIUS
            self.vy = -abs(self.vy)

        # Оновлюємо фізичне розташування на Canvas
        self.canvas.coords(
            self.id,
            self.x - self.RADIUS, self.y - self.RADIUS,
            self.x + self.RADIUS, self.y + self.RADIUS
        )

class Application:
    """Клас, що відповідає за роботу всієї програми."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bouncing Balls Simulation")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)

        # Фрейм для кнопок
        self.control_frame = tk.Frame(self.root, bg="#2C3E50")
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        # Кнопка очищення
        self.clear_btn = tk.Button(
            self.control_frame, text="Очистити екран", 
            command=self.clear_canvas, 
            font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", relief=tk.FLAT
        )
        self.clear_btn.pack(pady=10)

        # Створення Canvas
        self.canvas = tk.Canvas(self.root, bg="#ECF0F1")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Обробники подій
        self.canvas.bind("<Button-1>", self.create_ball)
        self.canvas.bind("<Configure>", self.on_resize)

        # Стан програми (без глобальних змінних)
        self.balls = []
        self.width = 800
        self.height = 600

        # Запуск анімації
        self.animate()

    def on_resize(self, event):
        """Адаптує розміри полотна при зміні розміру вікна."""
        self.width = event.width
        self.height = event.height

    def create_ball(self, event):
        """Створює нову кульку в місці кліку."""
        new_ball = Ball(self.canvas, event.x, event.y)
        self.balls.append(new_ball)

    def clear_canvas(self):
        """Видаляє всі кульки з екрана та очищає список."""
        self.canvas.delete("all")
        self.balls.clear()

    def resolve_collisions(self):
        """Перевіряє та обробляє зіткнення кульок між собою (Пружне зіткнення)."""
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                b1 = self.balls[i]
                b2 = self.balls[j]
                
                dx = b1.x - b2.x
                dy = b1.y - b2.y
                dist = math.hypot(dx, dy)
                min_dist = b1.RADIUS + b2.RADIUS

                if dist < min_dist:
                    # Щоб уникнути ділення на нуль
                    if dist == 0:
                        dist = 0.1

                    # 1. Розштовхуємо кульки, щоб вони не "злипалися"
                    overlap = 0.5 * (min_dist - dist)
                    nx = dx / dist
                    ny = dy / dist

                    b1.x += nx * overlap
                    b1.y += ny * overlap
                    b2.x -= nx * overlap
                    b2.y -= ny * overlap

                    # 2. Обмінюємося векторами швидкостей вздовж нормалі зіткнення
                    dpNorm1 = b1.vx * nx + b1.vy * ny
                    dpNorm2 = b2.vx * nx + b2.vy * ny

                    dpTan1 = b1.vx * -ny + b1.vy * nx
                    dpTan2 = b2.vx * -ny + b2.vy * nx

                    b1.vx = dpNorm2 * nx - dpTan1 * ny
                    b1.vy = dpNorm2 * ny + dpTan1 * nx
                    
                    b2.vx = dpNorm1 * nx - dpTan2 * ny
                    b2.vy = dpNorm1 * ny + dpTan2 * nx

    def animate(self):
        """Цикл анімації."""
        self.resolve_collisions()
        
        for ball in self.balls:
            ball.move(self.width, self.height)
            
        # Зациклюємо анімацію (~60 кадрів на секунду)
        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()