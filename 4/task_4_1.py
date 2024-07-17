import math


# Функция, которую мы будем использовать для поиска корня
def f(x):
    return x ** 2 * math.cos(x) + math.sin(x)


# Функция для поиска интервала изменения знака функции
def find_sign_change_interval(start, end, step):
    a = start
    b = start + step
    while b <= end:
        # Если произведение значений функции в точках a и b меньше нуля, значит, знаки разные
        if f(a) * f(b) < 0:
            return a, b
        a = b
        b += step
    raise ValueError("Не найдено изменение знака в заданном интервале")


# Функция метода бисекции для нахождения корня функции
def bisection_method(a, b, tol):
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) и f(b) должны иметь противоположные знаки")

    c = a
    while (b - a) / 2.0 > tol:
        c = (a + b) / 2.0
        # Если значение функции в точке c равно нулю, мы нашли корень
        if f(c) == 0:
            break
        # Если значение функции в точках a и c имеют разные знаки, то корень находится между a и c
        elif f(a) * f(c) < 0:
            b = c
        # Иначе корень находится между c и b
        else:
            a = c
    return c


# Интервал для поиска изменения знака
search_start = 0.5
search_end = 10
step = 0.1

# Уровень точности
tol = 1e-7

try:
    # Поиск интервала изменения знака функции
    a, b = find_sign_change_interval(search_start, search_end, step)
    # Поиск корня функции методом бисекции
    root = bisection_method(a, b, tol)
    print(f"Корень функции: {root}")
except ValueError as e:
    print(e)
