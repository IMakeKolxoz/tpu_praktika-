import tkinter as tk
import random
import numpy as np
from math import sin, cos, pi


# Function to calculate Lagrange interpolation polynomial
def lagrange_interpolation(x, x_points, y_points):
    total = 0
    n = len(x_points)
    for i in range(n):
        xi, yi = x_points[i], y_points[i]
        term = yi
        for j in range(n):
            if i != j:
                term *= (x - x_points[j]) / (xi - x_points[j])
        total += term
    return total


# Main application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-window Application")
        self.geometry("400x200")

        btn1 = tk.Button(self, text="Движение по окружности", command=self.open_circle_in_circle)
        btn1.pack(pady=10)

        btn2 = tk.Button(self, text="Движение по спирали(постоянный радиус точки)",
                         command=self.open_circle_in_spiral_constant)
        btn2.pack(pady=10)

        btn3 = tk.Button(self, text="Движение по спирали(меняющийся радиус точки)",
                         command=self.open_circle_in_spiral_variable)
        btn3.pack(pady=10)

        btn4 = tk.Button(self, text="Движение по траектории", command=self.open_cyclic_movement)
        btn4.pack(pady=10)

    def open_circle_in_circle(self):
        CircleInCircleWindow(self)

    def open_circle_in_spiral_constant(self):
        CircleInSpiralConstantWindow(self)

    def open_circle_in_spiral_variable(self):
        CircleInSpiralVariableWindow(self)

    def open_cyclic_movement(self):
        CyclicMovementWindow(self)


class CircleInCircleWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Движение по окружности")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, width=1000, height=1000, bg='white')
        self.canvas.pack()

        self.radius = 100
        self.angle = 0

        self.update_position()

    def update_position(self):
        center_x, center_y = 400, 300
        x = center_x + self.radius * cos(self.angle)
        y = center_y + self.radius * sin(self.angle)
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='red')
        self.angle += 0.05
        self.after(50, self.update_position)


class CircleInSpiralConstantWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Движение по спирали(постоянный радиус точки)")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, width=1000, height=1000, bg='white')
        self.canvas.pack()

        self.radius = 1
        self.angle = 0

        self.update_position()

    def update_position(self):
        center_x, center_y = 400, 300
        x = center_x + self.radius * cos(self.angle)
        y = center_y + self.radius * sin(self.angle)
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='red')
        self.angle += 0.1
        self.radius += 0.5
        self.after(50, self.update_position)


class CircleInSpiralVariableWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Движение по спирали(меняющийся радиус точки)")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, width=1000, height=1000, bg='white')
        self.canvas.pack()

        self.radius = 10
        self.angle = 1

        self.x_up = 10
        self.y_up = 10

        self.update_position()

    def update_position(self):
        center_x, center_y = 400, 300
        x = center_x + self.radius * cos(self.angle)
        y = center_y + self.radius * sin(self.angle)
        self.canvas.create_oval(x - self.x_up, y - self.y_up, x + self.x_up, y + self.y_up, fill='red')

        self.x_up += 0.5
        self.y_up += 0.5

        self.angle += 0.1
        self.radius += 1
        self.after(50, self.update_position)


class CyclicMovementWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Движение по траектории")
        self.geometry("1000x1000")

        self.canvas = tk.Canvas(self, width=1000, height=1000, bg='white')
        self.canvas.pack()

        self.num_points = random.randint(5, 10)
        self.x_points = [random.randint(50, 750) for _ in range(self.num_points)]
        self.y_points = [random.randint(50, 550) for _ in range(self.num_points)]

        self.trajectory_x = np.linspace(min(self.x_points), max(self.x_points), 1000)
        self.trajectory_y = [lagrange_interpolation(x, self.x_points, self.y_points) for x in self.trajectory_x]

        self.current_index = 0
        self.speed = 10

        self.draw_trajectory()
        self.animate()

    def draw_trajectory(self):
        for i in range(len(self.trajectory_x) - 1):
            self.canvas.create_line(self.trajectory_x[i], self.trajectory_y[i], self.trajectory_x[i + 1],
                                    self.trajectory_y[i + 1], fill='blue')

    def animate(self):
        if self.current_index < len(self.trajectory_x):
            x = self.trajectory_x[self.current_index]
            y = self.trajectory_y[self.current_index]
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red', outline='red')
            self.current_index += self.speed
            self.after(50, self.animate)
        else:
            self.current_index = 0
            self.animate()


if __name__ == "__main__":
    app = App()
    app.mainloop()
