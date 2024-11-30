import numpy as np
from config import *
from numba import njit, prange

# Calculate spacing between slots
spacing = (W - N_slots * slot_w) / (N_slots + 1)

# Generate slot positions
slot_positions = spacing + np.arange(N_slots) * (slot_w + spacing)
slots = np.array(
    [slot_positions, np.zeros(N_slots), np.full(N_slots, slot_w), np.full(N_slots, H)]
).T

# Precompute angles for the coin vertices (shape of the coin)
angles = np.linspace(0, 2 * np.pi, S, endpoint=False)


@njit(parallel=True)
def simulate_batch(batch_size, slots, angles):
    successes = np.zeros(batch_size, dtype=np.bool_)
    N_slots = slots.shape[0]
    S = angles.shape[0]

    for i in prange(batch_size):
        x_center = np.random.uniform(0, W)
        y_center = np.random.uniform(0, H)
        theta = np.random.uniform(0, 2 * np.pi)

        # Compute rotated angles
        rotated_angles = angles + theta

        # Generate coin vertices
        x_vertices = x_center + R * np.cos(rotated_angles)
        y_vertices = y_center + R * np.sin(rotated_angles)

        # Check if coin is entirely within any slot
        for s in range(N_slots):
            x0, y0, sw, sh = slots[s]
            x1 = x0 + sw
            y1 = y0 + sh

            # Check if all vertices are within the slot
            in_slot = True
            for k in range(S):
                xv = x_vertices[k]
                yv = y_vertices[k]
                if not (xv >= x0 and xv <= x1 and yv >= y0 and yv <= y1):
                    in_slot = False
                    break  # Exit early if any vertex is outside
            if in_slot:
                successes[i] = True
                break  # No need to check other slots

    return successes


# Set batch size (adjust based on your system's memory capacity)
batch_size = 1_000_000  # For example, 1 million simulations per batch

# Calculate the number of full batches and any remaining simulations
num_batches = num_simulations // batch_size
remaining = num_simulations % batch_size

total_successes = 0

# Process full batches
for _ in range(num_batches):
    successes = simulate_batch(batch_size, slots, angles)
    total_successes += successes.sum()

# Process any remaining simulations
if remaining > 0:
    successes = simulate_batch(remaining, slots, angles)
    total_successes += successes.sum()

# Calculate and print the estimated probability
estimated_probability = total_successes / num_simulations
print(f"Estimated Probability: {estimated_probability}")
