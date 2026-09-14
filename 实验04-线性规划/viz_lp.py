import numpy as np
import matplotlib.pyplot as plt

def plot_linear_programming_with_objective(figsize=(8, 8), show_grid=True):
    """
    Plot the feasible region for a linear programming problem with constraints:
    - x + y ≤ 4
    - 2x + y ≤ 5
    - x ≥ 0
    - y ≥ 0

    And objective function z = 3x + y

    Parameters:
    -----------
    figsize : tuple, optional
        Figure size (width, height). Default is (8, 8)
    show_grid : bool, optional
        Whether to show grid lines. Default is True

    Returns:
    --------
    fig, ax : matplotlib figure and axis objects
    vertices : list
        List of vertex coordinates of the feasible region
    optimal_point : list
        Coordinates of the optimal point
    optimal_value : float
        Optimal value of the objective function
    """

    # Define the constraints
    x = np.linspace(0, 5, 400)
    y = np.linspace(0, 5, 400)

    # Constraint lines
    y1 = 4 - x  # x + y = 4
    y2 = 5 - 2 * x  # 2x + y = 5

    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)

    # Plot the constraints
    plt.plot(x, y1, label=r'$x + y \leq 4$', color='blue', linewidth=2)
    plt.plot(x, y2, label=r'$2x + y \leq 5$', color='green', linewidth=2)
    plt.axhline(0, label=r'$y \geq 0$', color='red', linewidth=2)
    plt.axvline(0, label=r'$x \geq 0$', color='orange', linewidth=2)

    # Fill feasible region
    y3 = np.minimum(y1, y2)
    ax.fill_between(x, 0, y3, where=(y3 >= 0), color='lightblue', alpha=0.3, label='Feasible Region')

    # Find intersection points (vertices)
    vertices = []

    # 1. Origin (0, 0)
    vertices.append([0, 0])

    # 2. Intersection of x = 0 and x + y = 4
    vertices.append([0, 4])

    # 3. Intersection of x + y = 4 and 2x + y = 5
    # Solving: x + y = 4 and 2x + y = 5
    # Subtracting: x = 1, so y = 3
    vertices.append([1, 3])

    # 4. Intersection of 2x + y = 5 and y = 0
    # 2x + 0 = 5, so x = 2.5
    vertices.append([2.5, 0])

    # Calculate objective function values at vertices
    objective_values = []
    for vertex in vertices:
        z = 3 * vertex[0] + vertex[1]
        objective_values.append(z)

    # Find optimal point (maximum value)
    max_idx = np.argmax(objective_values)
    optimal_point = vertices[max_idx]
    optimal_value = objective_values[max_idx]

    # Highlight vertices with different colors based on objective function value
    colors = plt.cm.viridis(np.linspace(0, 1, len(vertices)))
    for i, (vertex, obj_val, color) in enumerate(zip(vertices, objective_values, colors)):
        marker = 'D' if i == max_idx else 'o'  # Diamond for optimal point
        size = 12 if i == max_idx else 8
        ax.plot(vertex[0], vertex[1], marker=marker, color=color, markersize=size,
                markeredgecolor='black', markeredgewidth=1.5)

        # Add annotation
        coord_str = f'({vertex[0]:.1f}, {vertex[1]:.1f})\nz = {obj_val:.1f}'
        if i == max_idx:
            coord_str += '\n(Optimal)'

        ax.annotate(coord_str, (vertex[0], vertex[1]),
                   xytext=(-30, 10), textcoords='offset points',
                   fontsize=9, ha='left',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    # Add objective function contour lines
    X, Y = np.meshgrid(np.linspace(0, 5, 100), np.linspace(0, 5, 100))
    Z = 3 * X + Y

    # Plot several contour lines
    contour_levels = np.linspace(0, optimal_value * 1.2, 8)
    contours = ax.contour(X, Y, Z, levels=contour_levels, colors='gray', alpha=0.6, linestyles='--')
    ax.clabel(contours, inline=True, fontsize=8, fmt='z=%.1f')

    # Highlight the optimal contour line
    optimal_contour = ax.contour(X, Y, Z, levels=[optimal_value], colors='red', linewidths=3)
    # 修复：移除 fontweight 参数
    ax.clabel(optimal_contour, inline=True, fontsize=10, fmt='z=%.1f (Optimal)')

    # Add arrow showing direction of increasing objective function
    arrow_start = [0.5, 0.5]
    arrow_direction = [3, 1]  # Gradient direction of z = 3x + y
    arrow_length = 0.8
    arrow_end = [arrow_start[0] + arrow_length * arrow_direction[0] / np.linalg.norm(arrow_direction),
                 arrow_start[1] + arrow_length * arrow_direction[1] / np.linalg.norm(arrow_direction)]

    ax.annotate('', xy=arrow_end, xytext=arrow_start,
                arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
    ax.text(arrow_end[0] + 0.1, arrow_end[1] + 0.1, 'Increasing z',
            color='purple', fontweight='bold', fontsize=10)

    # Set plot properties
    ax.set_xlim(-0.2, 5)
    ax.set_ylim(-0.2, 5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('LP Objective Function z = 3x + y',
                fontsize=14, fontweight='bold')

    # Add legend
    ax.legend(loc='upper right')

    # Show grid if requested
    if show_grid:
        ax.grid(True, alpha=0.3)

    # Make axes more prominent
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)

    plt.tight_layout()

    return fig, ax, vertices, optimal_point, optimal_value

def example_usage_with_objective():
    """
    Example of how to use the plotting function with objective function
    """
    print("LP Objective Function z = 3x + y...")
    fig, ax, vertices, optimal_point, optimal_value = plot_linear_programming_with_objective(figsize=(8, 6))

    print("\n" + "="*50)
    print("LINEAR PROGRAMMING SOLUTION")
    print("="*50)
    print("Constraints:")
    print("  x + y ≤ 4")
    print("  2x + y ≤ 5")
    print("  x ≥ 0, y ≥ 0")
    print(f"\nObjective Function: Maximize z = 3x + y")

    print(f"\nVertices of the feasible region:")
    for i, vertex in enumerate(vertices):
        z_val = 3 * vertex[0] + vertex[1]
        status = " ← OPTIMAL" if vertex == optimal_point else ""
        print(f"  Vertex {i+1}: ({vertex[0]:.1f}, {vertex[1]:.1f}), z = {z_val:.1f}{status}")

    print(f"\nOptimal Solution:")
    print(f"  Point: ({optimal_point[0]:.1f}, {optimal_point[1]:.1f})")
    print(f"  Maximum Value: z = {optimal_value:.1f}")
    print("="*50)

    plt.show()
    return fig, ax, vertices, optimal_point, optimal_value

if __name__ == "__main__":
    example_usage_with_objective()