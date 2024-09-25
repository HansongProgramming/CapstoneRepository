import numpy as np
from mayavi import mlab

# Example bloodstain data (replace this with real data from image analysis)
bloodstains = np.random.rand(50, 3)  # 50 bloodstains with (x, y, z) coordinates

# Example point of convergence (replace with calculated point of origin)
convergence_point = np.array([0.5, 0.5, 0.5])

# Create a new Mayavi figure
mlab.figure(size=(600, 600), bgcolor=(1, 1, 1))

# Plot bloodstains as red spheres in 3D space
mlab.points3d(bloodstains[:, 0], bloodstains[:, 1], bloodstains[:, 2],
              color=(1, 0, 0), scale_factor=0.05, resolution=20, name="Blood Stains")

# Plot the point of convergence as a larger blue sphere
mlab.points3d(convergence_point[0], convergence_point[1], convergence_point[2],
              color=(0, 0, 1), scale_factor=0.1, resolution=50, name="Point of Convergence")

# Optionally, draw lines from each bloodstain to the point of convergence
for stain in bloodstains:
    mlab.plot3d([stain[0], convergence_point[0]],
                [stain[1], convergence_point[1]],
                [stain[2], convergence_point[2]],
                color=(0.5, 0.5, 0.5), tube_radius=0.005, opacity=0.6)

# Set axis labels
mlab.axes(xlabel='X', ylabel='Y', zlabel='Z', color=(0, 0, 0))

# Show the plot
mlab.show()
