import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
x = np.linspace(0, 5, 400)

# Constraint lines
y1 = 4 - x
y2 = 5 - 2*x

# Plot the constraints
plt.figure(figsize=(8, 8))
plt.plot(x, y1, label=r'$x + y \leq 4$', color='b')
plt.plot(x, y2, label=r'$2x + y \leq 5$', color='r')

# Fill feasible region
y3 = np.minimum(y1, y2)
plt.fill_between(x, 0, y3, where=(y3 >= 0), color='gray', alpha=0.5, label='Feasible Region')

# Add labels and title
plt.xlim(0, 5)
plt.ylim(0, 5)
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