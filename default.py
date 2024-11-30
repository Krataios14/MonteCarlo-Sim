import numpy as np
from config import *


# Calculate spacing between slots
spacing = (W - N_slots * slot_w) / (N_slots + 1)

# Generate slot positions
slot_positions = spacing + np.arange(N_slots) * (slot_w + spacing)
slots = np.array(
    [slot_positions, np.zeros(N_slots), np.full(N_slots, slot_w), np.full(N_slots, H)]
).T

# Precompute angles for the coin vertices (shape of the coin)
angles = np.linspace(0, 2 * np.pi, S, endpoint=False)

# Generate random positions and orientations for all simulations
x_centers = np.random.uniform(0, W, num_simulations)
y_centers = np.random.uniform(0, H, num_simulations)
thetas = np.random.uniform(
    0, 2 * np.pi, num_simulations
)  # Random orientations for the coins

# Compute rotated angles for all simulations (coin orientations)
rotated_angles = angles.reshape(1, -1) + thetas.reshape(-1, 1)

# Generate coin vertices for all simulations with random orientations
x_vertices = x_centers.reshape(-1, 1) + R * np.cos(rotated_angles)
y_vertices = y_centers.reshape(-1, 1) + R * np.sin(rotated_angles)

# Initialize success array
successes = np.zeros(num_simulations, dtype=bool)

# Check for each slot
for slot in slots:
    x0, y0, sw, sh = slot
    # Check if all vertices are within the slot for all simulations
    in_slot = np.all(
        (x_vertices >= x0)
        & (x_vertices <= x0 + sw)
        & (y_vertices >= y0)
        & (y_vertices <= y0 + sh),
        axis=1,
    )
    # Update successes
    successes |= in_slot

# Calculate and print the estimated probability
estimated_probability = np.mean(successes)
print(f"Estimated Probability: {estimated_probability}")
