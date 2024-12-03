import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import matplotlib.animation as animation
import random
from config import *

# Calculate spacing between slots
spacing = (W - N_slots * slot_w) / (N_slots + 1)

# Generate slot positions
slots = []
for i in range(N_slots):
    x = spacing + i * (slot_w + spacing)
    y = 0
    slots.append(Rectangle((x, y), slot_w, H))


# Function to generate coin vertices
def generate_coin(x_center, y_center, theta):
    angles = np.linspace(0, 2 * np.pi, S, endpoint=False) + theta
    x = x_center + R * np.cos(angles)
    y = y_center + R * np.sin(angles)
    return np.column_stack((x, y))


# Function to check if coin is entirely within a slot
def coin_in_slot(coin_vertices, slot):
    x0, y0 = slot.get_xy()
    sw, sh = slot.get_width(), slot.get_height()
    
    # Check which vertices are within the slot
    within_slot = (
        (coin_vertices[:, 0] >= x0)
        & (coin_vertices[:, 0] <= x0 + sw)
        & (coin_vertices[:, 1] >= y0)
        & (coin_vertices[:, 1] <= y0 + sh)
    )
    
    # Calculate the percentage of vertices inside the slot
    percentage_in_slot = np.sum(within_slot) / len(coin_vertices)
    
    # Return True if the percentage meets or exceeds the threshold
    return percentage_in_slot >= R_P



# Simulation
successes = 0
fig, ax = plt.subplots()


def simulate(i):
    simulate.count += 1  # Increment the simulation count
    ax.clear()
    # Randomly position the coin
    x_center = random.uniform(0, W)
    y_center = random.uniform(0, H)
    theta = random.uniform(0, 2 * np.pi)
    coin_vertices = generate_coin(x_center, y_center, theta)
    coin_polygon = Polygon(
        coin_vertices, closed=True, edgecolor="blue", facecolor="cyan", alpha=0.5
    )

    # Check if the coin is entirely within any slot
    fall_through = False
    for slot in slots:
        if coin_in_slot(coin_vertices, slot):
            # Slot turns green if the coin falls into it
            ax.add_patch(
                Rectangle(
                    slot.get_xy(),
                    slot.get_width(),
                    slot.get_height(),
                    edgecolor="red",
                    facecolor="green",  # Slot becomes green
                    alpha=0.5,
                )
            )
            fall_through = True
        else:
            # Default slot color
            ax.add_patch(
                Rectangle(
                    slot.get_xy(),
                    slot.get_width(),
                    slot.get_height(),
                    edgecolor="red",
                    facecolor="yellow",  # Slot color is yellow
                    alpha=0.5,
                )
            )


    # Draw grating
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), W, H, edgecolor="black", facecolor="none"))

    # Draw slots
    for slot in slots:
        ax.add_patch(
            Rectangle(
                slot.get_xy(),
                slot.get_width(),
                slot.get_height(),
                edgecolor="red",
                facecolor="none",
            )
        )

    # Draw coin
    ax.add_patch(coin_polygon)

    # Update success count
    if fall_through:
        ax.set_title(f"Simulation {i+1}: Coin falls through!")
        simulate.successes += 1
    else:
        ax.set_title(f"Simulation {i+1}: Coin does not fall through.")

    # Display counts
    ax.text(
        0.02 * W,
        0.95 * H,
        f"Successes: {simulate.successes}/{simulate.count}",
        fontsize=12,
        color="green",
    )


simulate.successes = 0
simulate.count = 0  # Initialize the simulation count

# Handler for window close event
def handle_close(evt):
    if simulate.count > 0:
        estimated_probability = simulate.successes / simulate.count
        print(f"Estimated Probability: {estimated_probability}")
    else:
        print("No simulations run.")

# Connect the close event handler
fig.canvas.mpl_connect('close_event', handle_close)

ani = animation.FuncAnimation(fig, simulate, frames=num_simulations, repeat=False)
plt.show()
