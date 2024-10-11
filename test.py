import cv2
import numpy as np
import math
import pyvista as pv

# Global variables for panning and zooming
zoom_scale = 1.0
pan_offset_x, pan_offset_y = 0, 0
drag_start_x, drag_start_y = -1, -1
dragging = False

# Mouse callback function to handle panning and zooming
def mouse_callback(event, x, y, flags, param):
    global pan_offset_x, pan_offset_y, zoom_scale, drag_start_x, drag_start_y, dragging
    
    if event == cv2.EVENT_MOUSEWHEEL:  # Zooming with mouse wheel
        zoom_center_x, zoom_center_y = x, y
        
        if flags > 0:  # Scroll up -> Zoom in
            zoom_scale = min(zoom_scale * 1.1, 10)
        else:  # Scroll down -> Zoom out
            zoom_scale = max(zoom_scale * 0.9, 0.1)
    
    if event == cv2.EVENT_LBUTTONDOWN:  # Start panning
        drag_start_x, drag_start_y = x, y
        dragging = True
    
    elif event == cv2.EVENT_MOUSEMOVE:  # Panning
        if dragging:
            pan_offset_x += x - drag_start_x
            pan_offset_y += y - drag_start_y
            drag_start_x, drag_start_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:  # End panning
        dragging = False

# Load the image
image = cv2.imread('blood_splatter.jpg')

# Create copies of the original image for different layers
image_with_satellite_points = image.copy()
image_with_lines = image.copy()
image_original = image.copy()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Threshold the image to separate the blood stains from the background
_, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find contours of the bloodstains
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create an empty list to store bloodstain coordinates
bloodstain_2d = []

# Loop over each contour (each detected bloodstain)
for i, cnt in enumerate(contours):
    # Compute the center of the contour using moments
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        # Store the 2D bloodstain position (assume z = 0 for now)
        bloodstain_2d.append((cx, cy, 0))  # 2D points with z as 0 initially

        # Draw a square (tracker) at the center of each bloodstain (satellite points)
        cv2.rectangle(image_with_satellite_points, (cx-5, cy-5), (cx+5, cy+5), color=(0, 255, 0), thickness=2)
        cv2.rectangle(image_with_lines, (cx-5, cy-5), (cx+5, cy+5), color=(0, 255, 0), thickness=2)

        # Label the stains for easy identification
        cv2.putText(image_with_satellite_points, f"{i+1}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image_with_lines, f"{i+1}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Function to apply zoom and pan
def apply_zoom_and_pan(img):
    h, w = img.shape[:2]
    
    # Calculate new size based on zoom scale
    new_w = int(w * zoom_scale)
    new_h = int(h * zoom_scale)
    
    # Resize image according to the zoom scale
    zoomed_image = cv2.resize(img, (new_w, new_h))
    
    # Calculate offsets for panning within image bounds
    max_x_offset = max(0, new_w - w)
    max_y_offset = max(0, new_h - h)
    offset_x = min(max(pan_offset_x, -max_x_offset), max_x_offset)
    offset_y = min(max(pan_offset_y, -max_y_offset), max_y_offset)

    # Crop the image based on the panned offset
    return zoomed_image[max(0, offset_y):min(new_h, h + offset_y), max(0, offset_x):min(new_w, w + offset_x)]

# Layer switching
layers = ["Original", "Satellite Points", "Lines"]
layer_images = [image_original, image_with_satellite_points, image_with_lines]
current_layer_index = 0

# Create a window for toggling layers
cv2.namedWindow('Blood Splatter Analysis')

# Set mouse callback for panning and zooming
cv2.setMouseCallback('Blood Splatter Analysis', mouse_callback)

while True:
    # Get the current layer image and apply zoom and pan
    zoomed_image = apply_zoom_and_pan(layer_images[current_layer_index])

    # Display the current layer image
    cv2.imshow('Blood Splatter Analysis', zoomed_image)

    key = cv2.waitKey(10)

    # Exit on ESC key
    if key == 27:
        break
    # Toggle layer with spacebar
    elif key == ord(' '):
        current_layer_index = (current_layer_index + 1) % len(layers)

cv2.destroyAllWindows()

# ----- Part 2: 3D Visualization using PyVista -----

# Now start the 3D plotting after the 2D window closes

# Convert 2D data (with z=0) to a NumPy array for PyVista
bloodstains = np.array(bloodstain_2d)

# Example point of convergence (replace with calculated point of origin)
convergence_point = np.array([0.5, 0.5, 0.5])  # Dummy example

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
