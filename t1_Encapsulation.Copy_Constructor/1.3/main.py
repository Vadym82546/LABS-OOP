import math
import glob

class Triangle:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
    def perimeter(self):
        return self.a + self.b + self.c
    def area(self):
        if self.a + self.b <= self.c or self.a + self.c <= self.b or self.b + self.c <= self.a:
            return 0
        p = self.perimeter() / 2
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

class Rectangle:
    def __init__(self, a, b):
        self.a, self.b = a, b
    def perimeter(self):
        return 2 * (self.a + self.b)
    def area(self):
        return self.a * self.b

class Trapeze:
    def __init__(self, a, b, m, n): 
        self.a, self.b, self.m, self.n = a, b, m, n
    def perimeter(self): 
        return self.a + self.b + self.m + self.n
    def area(self):
        a, b = (self.b, self.a) if self.b > self.a else (self.a, self.b)
        d = a - b
        if d == 0:
            return 0
        core = (d + self.m + self.n) * (d + self.m - self.n) * (d - self.m + self.n) * (-d + self.m + self.n)
        return 0 if core <= 0 else ((a + b) / (4 * d)) * math.sqrt(core)

class Parallelogram:
    def __init__(self, a, b, h):
        self.a, self.b, self.h = a, b, h
    def perimeter(self):
        return 2 * (self.a + self.b)
    def area(self):
        return self.a * self.h

class Circle:
    def __init__(self, r):
        self.r = r
    def perimeter(self):
        return self.r * 2 * math.pi
    def area(self):
        return math.pi * (self.r ** 2)

# Словник для встановлення відповідності між словом в інпут файлі 
# та классом в коді та кількістю аргументів для виклику методів
SHAPES = {
    'Rectangle': (2, Rectangle), 'Parallelogram': (3, Parallelogram),
    'Triangle': (3, Triangle), 'Trapeze': (4, Trapeze), 'Circle': (1, Circle)
}

def analyze_shapes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tokens = [t for t in f.read().split()]
    
    shapes, i = [], 0
    while i < len(tokens):
        name = tokens[i]
        # Коли зустрічається назва класу, программа бере з SHAPES інформацію 
        # скільки взяти наступних елементів зі списку tokens (де знаходяться всі
        # прочитані слова\числа) щоб занести їх (числа) до списку args, який буде
        # використовуватися для виклику необхідних методів класу (клас також береться з SHAPES)
        if name in SHAPES:
            count, ShapeClass = SHAPES[name]
            # блок try except, якщо зустрінуться у файлі недопустимі символи\слова
            try:
                args_tokens = []
                j = i + 1
                # Цикл буде додавати ВСЕ до args, поки не знайде назву фігури
                while j < len(tokens) and tokens[j] not in SHAPES:
                    args_tokens.append(tokens[j])
                    j += 1
                
                args = list(map(float, args_tokens))
                # Перевірка "> 0" для довжин та перевірка кількості параметрів для певної фігури
                if len(args) == count and all(val > 0 for val in args):
                    obj = ShapeClass(*args)
                    shapes.append({'name': name, 'args': args, 'p': obj.perimeter(), 'a': obj.area()})
            except (ValueError, IndexError):
                pass
            i = j - 1
        i += 1
    
    if not shapes: return
    # Пошук максимальних значень площі та периметру
    max_p = max(shapes, key=lambda x: x['p'])
    max_a = max(shapes, key=lambda x: x['a'])
    
    print(f"Файл: {filepath}")
    print(f" Макс периметр: {max_p['name']} {max_p['args']} -> {max_p['p']:.2f}")
    print(f" Макс площадь: {max_a['name']} {max_a['args']} -> {max_a['a']:.2f}\n")

# Виконує код для всіх файлів, які починаються на input та закінчуються на .txt
for file in glob.glob("input*.txt"):
    analyze_shapes(file)