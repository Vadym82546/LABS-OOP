import math
import glob
import os

class Figure:
    """Абстрактний базовий клас для всіх геометричних фігур."""
    def dimension(self):
        return None
    def perimeter(self):
        return None
    def square(self):
        return None
    def squareSurface(self):
        return None
    def squareBase(self):
        return None
    def height(self):
        return None
    def volume(self):
        return None

# Двовимірні фігури

class Triangle(Figure):
    def __init__(self, a, b, c):
        assert a > 0 and b > 0 and c > 0
        assert a + b > c and a + c > b and b + c > a, "Трикутник із такими сторонами не існує"
        self.a, self.b, self.c = a, b, c
    def dimension(self): return "2D"
    def perimeter(self): return self.a + self.b + self.c
    def square(self):
        p = (self.a + self.b + self.c) / 2
        val = p * (p - self.a) * (p - self.b) * (p - self.c)
        return math.sqrt(val) if val > 0 else 0
    def volume(self): return self.square()

class Rectangle(Figure):
    def __init__(self, a, b):
        assert a > 0 and b > 0
        self.a, self.b = a, b
    def dimension(self): return "2D"
    def perimeter(self): return 2 * (self.a + self.b)
    def square(self): return self.a * self.b
    def volume(self): return self.square()

class Trapeze(Figure):
    def __init__(self, a, b, m, n):
        assert a > 0 and b > 0 and m > 0 and n > 0
        d = abs(a - b)
        assert d > 0, "Основи трапеції не можуть бути рівними"
        assert m + n > d and d + m > n and d + n > m, "Трапеція з такими сторонами не існує"
        self.a, self.b, self.m, self.n = a, b, m, n
    def dimension(self): return "2D"
    def perimeter(self): return self.a + self.b + self.m + self.n
    def square(self):
        a_base, b_base = (self.b, self.a) if self.b > self.a else (self.a, self.b)
        d = a_base - b_base
        if d == 0: return 0
        core = (d + self.m + self.n) * (d + self.m - self.n) * (d - self.m + self.n) * (-d + self.m + self.n)
        return 0 if core <= 0 else ((a_base + b_base) / (4 * d)) * math.sqrt(core)
    def volume(self): return self.square()

class Parallelogram(Figure):
    def __init__(self, a, b, h):
        assert a > 0 and b > 0 and h > 0
        assert h <= b, "Висота не може бути більшою за бічну сторону"
        self.a, self.b, self.h = a, b, h
    def dimension(self): return "2D"
    def perimeter(self): return 2 * (self.a + self.b)
    def square(self): return self.a * self.h
    def volume(self): return self.square()

class Circle(Figure):
    def __init__(self, r):
        assert r > 0
        self.r = r
    def dimension(self): return "2D"
    def perimeter(self): return 2 * math.pi * self.r
    def square(self): return math.pi * (self.r ** 2)
    def volume(self): return self.square()

# Тривимірні фігури

class Ball(Figure):
    def __init__(self, r):
        assert r > 0
        self.r = r
    def dimension(self): return "3D"
    def squareSurface(self): return 4 * math.pi * (self.r ** 2)
    def volume(self): return (4/3) * math.pi * (self.r ** 3)

class TriangularPyramid(Figure):
    def __init__(self, a, h):
        assert h > 0
        self.base = Triangle(a, a, a)
        self.a = a
        self.h_val = h
    def dimension(self): return "3D"
    def squareBase(self): return self.base.square()
    def height(self): return self.h_val
    def volume(self): return (1/3) * self.squareBase() * self.h_val
    def squareSurface(self):
        r_in = self.a / (2 * math.sqrt(3))
        l = math.sqrt(self.h_val**2 + r_in**2)
        lateral_area = 0.5 * (3 * self.a) * l
        return lateral_area + self.squareBase()

class QuadrangularPyramid(Figure):
    def __init__(self, a, b, h):
        assert h > 0
        self.base = Rectangle(a, b)
        self.a, self.b = a, b
        self.h_val = h
    def dimension(self): return "3D"
    def squareBase(self): return self.base.square()
    def height(self): return self.h_val
    def volume(self): return (1/3) * self.squareBase() * self.h_val
    def squareSurface(self):
        l1 = math.sqrt(self.h_val**2 + (self.b/2)**2)
        l2 = math.sqrt(self.h_val**2 + (self.a/2)**2)
        lateral_area = self.a * l1 + self.b * l2
        return lateral_area + self.squareBase()

class RectangularParallelepiped(Figure):
    def __init__(self, a, b, c):
        assert c > 0, "Третє ребро має бути додатним"
        self.base = Rectangle(a, b)
        self.a, self.b = a, b
        self.c_val = c
    def dimension(self): return "3D"
    def squareBase(self): return self.base.square()
    def height(self): return self.c_val
    def volume(self): return self.squareBase() * self.c_val
    def squareSurface(self):
        return self.base.perimeter() * self.c_val + 2 * self.squareBase()

class Cone(Figure):
    def __init__(self, r, h):
        assert h > 0
        self.base = Circle(r)
        self.r = r
        self.h_val = h
    def dimension(self): return "3D"
    def squareBase(self): return self.base.square()
    def height(self): return self.h_val
    def volume(self): return (1/3) * self.squareBase() * self.h_val
    def squareSurface(self):
        l = math.sqrt(self.r**2 + self.h_val**2)
        lateral_area = math.pi * self.r * l
        return lateral_area + self.squareBase()

class TriangularPrism(Figure):
    def __init__(self, a, b, c, h):
        assert h > 0
        self.base = Triangle(a, b, c)
        self.h_val = h
    def dimension(self): return "3D"
    def squareBase(self): return self.base.square()
    def height(self): return self.h_val
    def volume(self): return self.squareBase() * self.h_val
    def squareSurface(self):
        return self.base.perimeter() * self.h_val + 2 * self.squareBase()

# Словник доступних фігур: (кількість параметрів, клас)
SHAPES = {
    'Triangle': (3, Triangle),
    'Rectangle': (2, Rectangle),
    'Trapeze': (4, Trapeze),
    'Parallelogram': (3, Parallelogram),
    'Circle': (1, Circle),
    'Ball': (1, Ball),
    'TriangularPyramid': (2, TriangularPyramid),
    'QuadrangularPyramid': (3, QuadrangularPyramid),
    'RectangularParallelepiped': (3, RectangularParallelepiped),
    'Cone': (2, Cone),
    'TriangularPrism': (4, TriangularPrism)
}

def analyze_shapes(filepath):
    """Обробляє файл та знаходить фігуру з найбільшою мірою (площею або об'ємом)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tokens = f.read().split()
    except Exception:
        return

    found_shapes = []
    i = 0
    while i < len(tokens):
        name = tokens[i]
        if name in SHAPES:
            count, ShapeClass = SHAPES[name]
            try:
                args_tokens = tokens[i+1 : i+1+count]
                args = list(map(float, args_tokens))
                
                if len(args) == count:
                    obj = ShapeClass(*args)
                    found_shapes.append({
                        'name': name,
                        'args': args,
                        'measure': obj.volume()
                    })
                    i += count # Перестрибуємо через зчитані аргументи
            except (ValueError, IndexError, AssertionError):
                pass
        i += 1
    
    if not found_shapes:
        return
    
    # Знаходження фігури з максимальним volume()
    max_fig = max(found_shapes, key=lambda x: x['measure'])
    
    print(f"Файл: {os.path.basename(filepath)}")
    print(f"Фігура з найбільшою мірою: {max_fig['name']} {max_fig['args']} -> {max_fig['measure']:.2f}\n")

if __name__ == "__main__":
    # Пошук файлів input*.txt у поточній папці
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(script_dir, "input*.txt")))
    
    for f in files:
        analyze_shapes(f)
