import numpy as np
import matplotlib.pyplot as plt

def plot_integer_linear_programming(figsize=(8, 8), show_grid=True):
    """
    Plot the feasible region for an Integer Linear Programming problem with constraints:
    - x + y ≤ 4
    - 2x + y ≤ 5
    - x ≥ 0
    - y ≥ 0

    And objective function z = 3x + y (Integer solutions only)
    """

    # ------------------------------------------------------------------ #
    #  1. Constraint lines — clipped to y ≥ 0                             #
    # ------------------------------------------------------------------ #
    x = np.linspace(0, 5, 400)

    y1 = 4 - x
    y2 = 5 - 2 * x

    y1_clipped = np.where(y1 >= 0, y1, np.nan)
    y2_clipped = np.where(y2 >= 0, y2, np.nan)

    # ------------------------------------------------------------------ #
    #  2. Enumerate every feasible integer point                          #
    # ------------------------------------------------------------------ #
    integer_points = []
    for xi in range(0, 6):
        for yi in range(0, 6):
            if (xi + yi <= 4) and (2 * xi + yi <= 5) and xi >= 0 and yi >= 0:
                integer_points.append([xi, yi])

    objective_values = [3 * p[0] + p[1] for p in integer_points]

    max_idx       = int(np.argmax(objective_values))
    optimal_point = integer_points[max_idx]
    optimal_value = objective_values[max_idx]

    # ------------------------------------------------------------------ #
    #  3. LP relaxation vertices                                          #
    # ------------------------------------------------------------------ #
    lp_vertices  = [[0, 0], [0, 4], [1, 3], [2.5, 0]]
    lp_obj_vals  = [3 * v[0] + v[1] for v in lp_vertices]

    # ------------------------------------------------------------------ #
    #  4. Build the figure                                                #
    # ------------------------------------------------------------------ #
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(x, y1_clipped, label=r'$x + y \leq 4$',  color='blue',  linewidth=2)
    ax.plot(x, y2_clipped, label=r'$2x + y \leq 5$', color='green', linewidth=2)
    ax.axhline(0, label=r'$y \geq 0$',  color='red',    linewidth=2)
    ax.axvline(0, label=r'$x \geq 0$',  color='orange', linewidth=2)

    y3 = np.minimum(y1, y2)
    ax.fill_between(x, 0, y3, where=(y3 >= 0),
                    color='lightblue', alpha=0.25,
                    label='LP Feasible Region (Relaxation)')

    # ------------------------------------------------------------------ #
    #  5. Objective-function contour lines                                #
    # ------------------------------------------------------------------ #
    X, Y = np.meshgrid(np.linspace(0, 5, 200), np.linspace(0, 5, 200))
    Z    = 3 * X + Y

    contour_levels = np.linspace(0, optimal_value * 1.2, 8)
    contours = ax.contour(X, Y, Z, levels=contour_levels,
                          colors='gray', alpha=0.5, linestyles='--')
    ax.clabel(contours, inline=True, fontsize=8, fmt='z=%.1f')

    # Optimal contour as a direct line
    x_opt = np.linspace(0, 5, 400)
    y_opt = optimal_value - 3 * x_opt
    mask  = (y_opt >= 0) & (y_opt <= 5)
    ax.plot(x_opt[mask], y_opt[mask],
            color='purple', linewidth=2.5, linestyle='-',
            label=f'Optimal Contour  z={optimal_value:.0f}')

    mid_idx = np.where(mask)[0][len(np.where(mask)[0]) // 2]
    ax.annotate(f'z={optimal_value:.1f} (ILP Optimal)',
                xy=(x_opt[mid_idx], y_opt[mid_idx]),
                xytext=(8, 8), textcoords='offset points',
                fontsize=9, color='purple', fontweight='bold')

    # ------------------------------------------------------------------ #
    #  6. LP relaxation vertices                                          #
    # ------------------------------------------------------------------ #
    for v, zv in zip(lp_vertices, lp_obj_vals):
        ax.plot(v[0], v[1], marker='D', color='none',
                markeredgecolor='steelblue', markeredgewidth=1.5,
                markersize=10, zorder=4)

    # ------------------------------------------------------------------ #
    #  7. All feasible integer points — colour-coded by z value           #
    # ------------------------------------------------------------------ #
    z_arr  = np.array(objective_values, dtype=float)
    z_norm = (z_arr - z_arr.min()) / (z_arr.max() - z_arr.min() + 1e-9)
    cmap   = plt.cm.YlOrRd

    for i, (pt, zv, zn) in enumerate(zip(integer_points, objective_values, z_norm)):
        is_optimal = (pt == optimal_point)

        marker     = '*'  if is_optimal else 'o'
        size       = 18   if is_optimal else 10
        edge_color = 'black'
        edge_width = 2.0  if is_optimal else 1.0
        color      = cmap(zn)

        ax.plot(pt[0], pt[1], marker=marker, color=color,
                markersize=size, markeredgecolor=edge_color,
                markeredgewidth=edge_width, zorder=5)

        label = f'({pt[0]}, {pt[1]})\nz={zv}'
        if is_optimal:
            label += '\n★ ILP Optimal'

        # ─── FIXED: place label to the RIGHT when x >= 2 ───────── #
        if pt[0] >= 2:
            x_offset = 15       # to the right of the point
            y_offset = 8
        else:
            x_offset = 8        # original position (to the left-ish)
            y_offset = 8

        ax.annotate(label, (pt[0], pt[1]),
                    xytext=(x_offset, y_offset),
                    textcoords='offset points',
                    fontsize=7.5, ha='left',
                    bbox=dict(boxstyle='round,pad=0.3',
                              facecolor='white', alpha=0.85,
                              edgecolor=edge_color,
                              linewidth=edge_width))

    # ------------------------------------------------------------------ #
    #  8. Colour-bar                                                      #
    # ------------------------------------------------------------------ #
    sm = plt.cm.ScalarMappable(cmap=cmap,
                                norm=plt.Normalize(vmin=z_arr.min(),
                                                   vmax=z_arr.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('Objective value  z = 3x + y', fontsize=9)

    # ------------------------------------------------------------------ #
    #  9. Gradient arrow                                                  #
    # ------------------------------------------------------------------ #
    grad      = np.array([3.0, 1.0])
    grad_unit = grad / np.linalg.norm(grad)
    a_start   = np.array([0.4, 0.4])
    a_end     = a_start + 0.9 * grad_unit

    ax.annotate('', xy=a_end, xytext=a_start,
                arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
    ax.text(a_end[0] + 0.08, a_end[1] + 0.08,
            'Increasing z', color='purple',
            fontweight='bold', fontsize=9)

    # ------------------------------------------------------------------ #
    #  10. Legend                                                          #
    # ------------------------------------------------------------------ #
    from matplotlib.lines import Line2D
    extra_handles = [
        Line2D([0], [0], marker='o', color='w',
               markerfacecolor=cmap(0.5), markeredgecolor='black',
               markersize=9, label='Feasible Integer Points'),
        Line2D([0], [0], marker='*', color='w',
               markerfacecolor=cmap(1.0), markeredgecolor='black',
               markersize=14, label='ILP Optimal Point'),
        Line2D([0], [0], marker='D', color='w',
               markerfacecolor='none', markeredgecolor='steelblue',
               markersize=9, label='LP Relaxation Vertices'),
        Line2D([0], [0], color='purple', linewidth=2.5,
               label=f'Optimal Contour  z={optimal_value:.0f}'),
    ]
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles + extra_handles,
              loc='upper right', fontsize=8)

    # ------------------------------------------------------------------ #
    #  11. Axes cosmetics                                                  #
    # ------------------------------------------------------------------ #
    ax.set_xlim(-0.4, 5)
    ax.set_ylim(-0.4, 5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Integer Linear Programming\nObjective: Maximize z = 3x + y',
                 fontsize=13, fontweight='bold')

    ax.axhline(0, color='black', lw=0.8)
    ax.axvline(0, color='black', lw=0.8)

    ax.set_xticks(range(6))
    ax.set_yticks(range(6))

    if show_grid:
        ax.grid(True, which='major', alpha=0.35, linestyle=':')

    plt.tight_layout()
    return fig, ax, integer_points, optimal_point, optimal_value


def example_usage_ilp():
    print("Solving Integer Linear Programme  z = 3x + y …")
    fig, ax, integer_points, optimal_point, optimal_value = \
        plot_integer_linear_programming(figsize=(9, 8))

    print("\n" + "=" * 55)
    print("  INTEGER LINEAR PROGRAMMING SOLUTION")
    print("=" * 55)
    print("  Constraints:")
    print("    x + y  ≤ 4")
    print("    2x + y ≤ 5")
    print("    x ≥ 0,  y ≥ 0,  x, y ∈ ℤ")
    print(f"\n  Objective: Maximize  z = 3x + y")
    print(f"\n  All feasible integer points ({len(integer_points)} total):")
    print(f"  {'Point':<15} {'z value':<10} {'Note'}")
    print("  " + "-" * 40)

    for pt in integer_points:
        zv   = 3 * pt[0] + pt[1]
        note = "← ILP OPTIMAL" if pt == optimal_point else ""
        print(f"  ({pt[0]}, {pt[1]}){'':<10} z = {zv:<6.1f} {note}")

    print(f"\n  Optimal Integer Solution:")
    print(f"    x* = {optimal_point[0]},  y* = {optimal_point[1]}")
    print(f"    z* = {optimal_value:.1f}")
    print("=" * 55)

    plt.show()
    return fig, ax, integer_points, optimal_point, optimal_value


if __name__ == "__main__":
    example_usage_ilp()