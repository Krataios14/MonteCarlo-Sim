import matplotlib.pyplot as plt
import numpy as np

num_simulations = 10000000  # Number of Monte Carlo simulations
h_min, h_max = 9.9530, 11.0470  # Bounds for h
o_min, o_max = 0, np.pi / 7  # Bounds for o

# Generate random samples for h and o
h_samples = np.random.uniform(h_min, h_max, num_simulations)
o_samples = np.random.uniform(o_min, o_max, num_simulations)

# Compute the condition 11.0470 * cos(o) < h
condition_met = h_samples > 11.0470 * np.cos(o_samples)

# Calculate the probability
probability = np.mean(condition_met)

print(probability)

# Generate data for visualization
o_values = np.linspace(o_min, o_max, 1000)
h_boundary = 11.0470 * np.cos(o_values)
# Reduce the number of samples plotted for better visualization
sample_indices = np.random.choice(len(o_samples), size=5000, replace=False)

# Use the reduced samples for plotting
reduced_o_samples = o_samples[sample_indices]
reduced_h_samples = h_samples[sample_indices]

# Plot the distributions and boundary with reduced data
plt.figure(figsize=(10, 6))

# Scatter plot of reduced samples
plt.scatter(reduced_o_samples, reduced_h_samples, s=1, alpha=0.3, label="Random Samples")

# Plot the boundary line
plt.plot(o_values, h_boundary, color='red', linewidth=2, label=r"Boundary: $h = 11.0470 \cdot \cos(o)$")

# Highlighting the region where h > boundary
plt.fill_between(o_values, h_boundary, h_max, color='red', alpha=0.2, label=r"Region where $h > 11.0470 \cdot \cos(o)$")

# Axis labels and legend
plt.xlabel(r"Angle $o$ (radians)", fontsize=12)
plt.ylabel(r"$h$ Value", fontsize=12)
plt.title(r"Monte Carlo Simulation: $h > 11.0470 \cdot \cos(o)$", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.show()
