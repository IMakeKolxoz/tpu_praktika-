import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x ** 4


def midpoint_rectangular_integration(f, a, b, n):
    h = (b - a) / n
    integral_sum = 0.0

    for i in range(n):
        mid_point = a + h * (i + 0.5)
        integral_sum += f(mid_point)

    integral_sum *= h
    return integral_sum


# Пределы интегрирования и функция
a = 0
b = 4

# Точное значение интеграла для проверки
exact_integral = (b ** 5 / 5) - (a ** 5 / 5)

# Заданная точность
epsilon = 1e-6

# Начальное значение N
N = 1

# Поиск оптимального N
while True:
    approx_integral = midpoint_rectangular_integration(f, a, b, N)
    error = abs(approx_integral - exact_integral)

    if error < epsilon:
        break

    N += 1

print(f"Оптимальное значение N: {N}")
print(f"Приближенное значение интеграла: {approx_integral}")
print(f"Точное значение интеграла: {exact_integral}")
print(f"Погрешность: {error}")

# Значения N для построения графика сходимости
N_values = np.arange(1, N + 1)
integral_values = [midpoint_rectangular_integration(f, a, b, n) for n in N_values]

# Построение графика функции
x = np.linspace(a, b, 400)
y = f(x)

plt.figure(figsize=(14, 6))

# График функции
plt.subplot(1, 2, 1)
plt.plot(x, y, label=r'$f(x) = x^4$')
plt.title('График функции $f(x) = x^4$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)

# График сходимости интегралов
plt.subplot(1, 2, 2)
plt.plot(N_values, integral_values, label='Приближенный интеграл')
plt.axhline(y=exact_integral, color='r', linestyle='-', label='Точный интеграл')
plt.title('График сходимости интегралов')
plt.xlabel('N (количество разбиений)')
plt.ylabel('Приближенное значение интеграла')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
