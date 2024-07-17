import math

# Функция, которую мы будем использовать для поиска корня
def f(x):
    return x ** 2 * math.cos(x) + math.sin(x)

# Производная функции f(x)
def df(x):
    return 2 * x * math.cos(x) - x ** 2 * math.sin(x) + math.cos(x)

# Функция метода Ньютона для нахождения корня функции
def newton_method(x0, tol, max_iter):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ValueError("Производная равна нулю, метод Ньютона не применим")
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("Метод Ньютона не сошелся за заданное количество итераций")

# Начальная точка
x0 = 1

# Уровень точности
tol = 1e-7

# Максимальное количество итераций
max_iter = 1000

try:
    # Поиск корня функции методом Ньютона
    root = newton_method(x0, tol, max_iter)
    print(f"Корень функции: {root}")
except ValueError as e:
    print(e)
