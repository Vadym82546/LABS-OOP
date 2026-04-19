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

class RationalList:
    def __init__(self, elements=None):
        self._elements = []
        if elements:
            for e in elements:
                self.append(e)

    def append(self, value):
        if isinstance(value, int):
            value = Rational(value, 1)
        if not isinstance(value, Rational):
            raise TypeError("Елементом списку може бути лише Rational або int")
        self._elements.append(value)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __setitem__(self, index, value):
        if isinstance(value, int):
            value = Rational(value, 1)
        if not isinstance(value, Rational):
            raise TypeError("Елементом списку може бути лише Rational або int")
        self._elements[index] = value

    def __add__(self, other):
        new_list = RationalList(self._elements)
        if isinstance(other, RationalList):
            for e in other._elements:
                new_list.append(e)
        elif isinstance(other, (Rational, int)):
            new_list.append(other)
        else:
            return NotImplemented
        return new_list

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            for e in other._elements:
                self.append(e)
        elif isinstance(other, (Rational, int)):
            self.append(other)
        else:
            return NotImplemented
        return self

    def __iter__(self):
        # Сортування: за знаменником (спадання), потім за чисельником (спадання)
        sorted_elements = sorted(self._elements, key=lambda r: (-r['d'], -r['n']))
        return iter(sorted_elements)

    def __str__(self):
        return "[" + ", ".join(str(e) for e in self._elements) + "]"

if __name__ == "__main__":
    for i in [1, 2, 3]:
        file = "input0" + str(i) + ".txt"
        rational_list = RationalList()
        try:
            with open(file, 'r') as f:
                for line in f:
                    for part in line.split():
                        rational_list.append(Rational(part) if '/' in part else Rational(int(part), 1))
            print("\nФайл input0" + str(i) + ".txt:")
            print(f"\nСума послідовності: {sum(rational_list._elements, Rational(0, 1))}")
            print("\nЕлементи списку (в порядку спадання знаменників):")
            for r in rational_list:
                print(r, end=" ")
        except FileNotFoundError:
            print(f"Файл {file} не знайдено.")