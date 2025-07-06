import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
x = np.linspace(0, 5, 400)
y = np.linspace(0, 5, 400)

# Constraint lines
y1 = 4 - x
y2 = 5 - 2 * x
y0 = 0 * x
x0 = 0 * y

# Plot the constraints
plt.figure(figsize=(8, 8))
plt.plot(x, y1, label=r'$x + y \leq 4$', color='b')
plt.plot(x, y2, label=r'$2x + y \leq 5$', color='g')
plt.plot(x, y0, label=r'$x \geq 0$', color='y')
plt.plot(x0, y, label=r'$y \geq 0$', color='m')

# Fill feasible region
y3 = np.minimum(y1, y2)
plt.fill_between(x, 0, y3, where=(y3 >= 0), color='gray', alpha=0.5, label='Feasible Region')

# Find intersection points (vertices)
# 1. Intersection of x + y = 4 and 2x + y = 5
A = np.array([[1, 1], [2, 1]])
b = np.array([4, 5])
intersection1 = np.linalg.solve(A, b)

# 2. Intersection of x + y = 4 and x = 0
intersection2 = [0, 4]

# 3. Intersection of 2x + y = 5 and y = 0
intersection3 = [2.5, 0]

# 4. Origin
intersection4 = [0, 0]

# Highlight the vertices
vertices = [intersection1, intersection2, intersection3, intersection4]
for vertex in vertices:
    plt.plot(vertex[0], vertex[1], 'ro', markersize=8, label=f'{vertex[0], vertex[1]}')  # 'ro' for red circles

# Add labels and title
plt.xlim(-0.1, 5)
plt.ylim(-0.1, 5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Programming Feasible Region')
plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)
plt.legend()

# Add title for the feasible region
plt.text(1, 1, 'Feasible Region', fontsize=12, color='black', ha='center')

# Show plot
plt.grid(True)
plt.show()