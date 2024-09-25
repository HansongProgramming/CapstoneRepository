import numpy as np
import pyvista as pv

# Example bloodstain data (replace this with real data from image analysis)
bloodstains = np.random.rand(50, 3)  # 50 bloodstains with (x, y, z) coordinates

# Example point of convergence (replace with calculated point of origin)
convergence_point = np.array([0.5, 0.5, 0.5])

# Create a PyVista plotter object
plotter = pv.Plotter()

# Plot bloodstains as red spheres
for stain in bloodstains:
    sphere = pv.Sphere(radius=0.02, center=stain)  # Radius controls the size of the sphere
    plotter.add_mesh(sphere, color='red', label='Blood Stains')

# Plot the point of convergence as a larger blue sphere
convergence_sphere = pv.Sphere(radius=0.05, center=convergence_point)
plotter.add_mesh(convergence_sphere, color='blue', label='Point of Convergence')

# Optionally, plot lines from each bloodstain to the point of convergence
for stain in bloodstains:
    line = pv.Line(stain, convergence_point)
    plotter.add_mesh(line, color='gray', line_width=2, opacity=0.5)

# Add axes and labels
plotter.add_axes()
plotter.show_bounds(grid='back', location="outer", all_edges=True)

# Display the 3D plot
plotter.show()
