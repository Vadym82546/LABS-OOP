import math

class Rational:
    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Rational):  # Конструктор копіювання
                self._n = arg._n
                self._d = arg._d
            elif isinstance(arg, str):     # Рядок типу 'n/d'
                try:
                    n_str, d_str = arg.split('/')
                    self._n = int(n_str)
                    self._d = int(d_str)
                except ValueError:
                    raise ValueError("Некоректний формат рядка. Очікується 'n/d'")
            else:
                raise TypeError("Очікується об'єкт Rational або рядок")
        elif len(args) == 2:               # Два цілих числа
            if isinstance(args[0], int) and isinstance(args[1], int):
                self._n = args[0]
                self._d = args[1]
            else:
                raise TypeError("Аргументи мають бути цілими числами")
        else:
            raise TypeError("Некоректна кількість аргументів")

        if self._d == 0:
            raise ZeroDivisionError("Знаменник не може бути нулем")
        
        self._simplify()

    def _simplify(self):
        """Метод для приведення дробу до нескоротного вигляду."""
        common = math.gcd(self._n, self._d)
        self._n //= common
        self._d //= common
        # Гарантуємо, що знак знаходиться у чисельнику
        if self._d < 0:
            self._n = -self._n
            self._d = -self._d

    # Допоміжний метод для перетворення іншого операнда в Rational
    def _to_rational(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other, 1)
        raise TypeError(f"Операція з типом {type(other)} не підтримується")

    # Арифметичні операції
    def __add__(self, other):
        other = self._to_rational(other)
        return Rational(self._n * other._d + other._n * self._d, self._d * other._d)

    def __sub__(self, other):
        other = self._to_rational(other)
        return Rational(self._n * other._d - other._n * self._d, self._d * other._d)

    def __mul__(self, other):
        other = self._to_rational(other)
        return Rational(self._n * other._n, self._d * other._d)

    def __truediv__(self, other):
        other = self._to_rational(other)
        if other._n == 0:
            raise ZeroDivisionError("Ділення на нуль (чисельник другого дробу дорівнює 0)")
        return Rational(self._n * other._d, self._d * other._n)

    # Оператор () — повертає десятковий дріб
    def __call__(self):
        return self._n / self._d

    # Оператор [] — доступ до чисельника та знаменника
    def __getitem__(self, key):
        if key == "n":
            return self._n
        elif key == "d":
            return self._d
        else:
            raise KeyError("Ключ має бути 'n' або 'd'")

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Значення має бути цілим числом")
        if key == "n":
            self._n = value
        elif key == "d":
            if value == 0:
                raise ZeroDivisionError("Знаменник не може бути нулем")
            self._d = value
        else:
            raise KeyError("Ключ має бути 'n' або 'd'")
        self._simplify()

    def __str__(self):
        return f"{self._n}/{self._d}"

    def __repr__(self):
        return f"Rational('{self._n}/{self._d}')"

# Функція для читання файлу та обчислень
def process_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Припускаємо, що у файлі записані вирази,
                # які можна обчислити, маючи клас Rational в контексті.
                # Для безпеки та гнучкості використовуємо eval з обмеженим scope.
                try:
                    result = eval(line, {"Rational": Rational, "math": math})
                    print(f"Вираз: {line}")
                    print(f"Результат: {result}")
                    print("-" * 20)
                except Exception as e:
                    print(f"Помилка при обчисленні '{line}': {e}")
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")

if __name__ == "__main__":
    process_file("input01.txt")