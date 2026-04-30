import math

def gen_a(x):
    """Генератор для послідовності a)"""
    k = 1
    term = x
    while True:
        yield term
        k += 1
        term = term * x * (k - 1) / k  # рекурентний перехід

def calc_a(x, k_target):
    """Обчислення k-го члена послідовності"""
    if k_target < 1:
        return None
    generator = gen_a(x)
    result = 0
    # Цикл з лічильником для досягнення потрібного члена
    for _ in range(k_target):
        result = next(generator)
    return result

print(calc_a(2, 3))


def gen_b():
    """Генератор для поточного добутку P_n"""
    i = 1
    p = 1
    while True:
        term = 1 / (i + math.factorial(1)) 
        p *= term
        yield p
        i += 1

def calc_b(n):
    """Обчислення добутку для заданого n"""
    if n < 1:
        return 1
    generator = gen_b()
    result = 1
    for _ in range(n):
        result = next(generator)
    return result

print(calc_b(2))


def gen_c():
    """Генератор визначників D_n"""
    d_prev2 = 2 # D_1
    yield d_prev2
    d_prev1 = 1 # D_2
    yield d_prev1
    
    while True:
        d_curr = 2 * d_prev1 - 3 * d_prev2 # рекурентна формула
        yield d_curr
        d_prev2, d_prev1 = d_prev1, d_curr

def calc_c(n):
    """Обчислення визначника порядку n"""
    if n < 1:
        return None
    generator = gen_c()
    result = 0
    for _ in range(n):
        result = next(generator)
    return result

print(calc_c(3))


def gen_d():
    """Генератор для поточних сум S_n"""
    a_prev2 = 0 # a_1
    a_prev1 = 1 # a_2
    
    # Для n=1
    power2 = 2
    s = power2 * a_prev2
    yield s
    
    # Для n=2
    k = 2
    power2 *= 2
    s += power2 * a_prev1
    yield s
    
    # Для n >= 3
    k = 3
    while True:
        a_curr = a_prev1 + k * a_prev2
        power2 *= 2
        s += power2 * a_curr
        yield s
        
        a_prev2, a_prev1 = a_prev1, a_curr
        k += 1

def calc_d(n):
    """Обчислення суми S_n"""
    if n < 1:
        return 0
    generator = gen_d()
    result = 0
    for _ in range(n):
        result = next(generator)
    return result

print(calc_d(3))


def gen_e(x):
    """Генератор членів ряду Тейлора для sin(x)"""
    n = 1
    term = x
    while True:
        yield term
        n += 1
        # Рекурентний перехід до наступного члена ряду
        term = term * (-x**2) / ((2 * n - 2) * (2 * n - 1))

def calc_e(x, eps):
    """Обчислення sin(x) з точністю eps за допомогою циклу з умовою"""
    generator = gen_e(x)
    sin_x = 0
    
    # Цикл з умовою (досягнення заданої точності)
    for term in generator:
        sin_x += term
        if abs(term) < eps:
            break
            
    math_sin = math.sin(x)
    print(f"Обчислене значення: {sin_x}")
    print(f"Значення math.sin:  {math_sin}")
    print(f"Різниця:            {abs(sin_x - math_sin)}")
    
    return sin_x

calc_e(math.pi / 4, 1e-6)