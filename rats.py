import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Example bloodstain data (replace this with real data from image analysis)
bloodstains = np.random.rand(50, 3)  # 50 bloodstains with (x, y, z) coordinates

# Example point of convergence (replace with calculated point of origin)
convergence_point = np.array([0.5, 0.5, 0.5])

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot bloodstains in 3D space
ax.scatter(bloodstains[:, 0], bloodstains[:, 1], bloodstains[:, 2], color='red', label='Blood Stains')

# Plot the point of convergence
ax.scatter(convergence_point[0], convergence_point[1], convergence_point[2], color='blue', s=100, label='Point of Convergence')

# Optionally, plot lines projecting from each stain to the point of convergence
for stain in bloodstains:
    ax.plot([stain[0], convergence_point[0]], [stain[1], convergence_point[1]], [stain[2], convergence_point[2]], color='gray', linestyle='--', alpha=0.5)

# Add labels and legend
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.legend()

plt.show()
