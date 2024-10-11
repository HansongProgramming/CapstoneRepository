import cv2
import numpy as np
import math

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

# Loop over each contour (each detected bloodstain)
for i, cnt in enumerate(contours):
    # Compute the center of the contour using moments
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Draw a square (tracker) at the center of each bloodstain (satellite points) on both images
        cv2.rectangle(image_with_satellite_points, (cx-5, cy-5), (cx+5, cy+5), color=(0, 255, 0), thickness=2)
        cv2.rectangle(image_with_lines, (cx-5, cy-5), (cx+5, cy+5), color=(0, 255, 0), thickness=2)

        # Label the stains for easy identification (main vs satellite)
        cv2.putText(image_with_satellite_points, f"{i+1}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image_with_lines, f"{i+1}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Fit an ellipse around the contour (if it has sufficient points)
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            (center, axes, angle) = ellipse
            major_axis = max(axes)
            minor_axis = min(axes)

            # Compute the angle of impact
            if major_axis != 0:
                angle_of_impact = math.degrees(math.asin(minor_axis / major_axis))
                
                # Draw the ellipse
                cv2.ellipse(image_with_lines, ellipse, (255, 255, 0), 2)

                # Display the angle of impact near the ellipse
                cv2.putText(image_with_lines, f"Angle: {int(angle_of_impact)}", (cx + 20, cy + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# OPTIONAL: Draw lines between the main bloodstain and its satellite stains on the "image_with_lines"
if contours:
    # Find the largest contour (assumed to be the main stain)
    main_stain = max(contours, key=cv2.contourArea)
    
    # Get the center of the main stain
    M_main = cv2.moments(main_stain)
    cx_main = int(M_main["m10"] / M_main["m00"])
    cy_main = int(M_main["m01"] / M_main["m00"])

    # Draw paths (lines) between the main stain and satellite stains on "image_with_lines"
    for cnt in contours:
        if cnt is not main_stain:  # Satellite stains
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # Draw a line from the main stain to each satellite stain
                cv2.line(image_with_lines, (cx_main, cy_main), (cx, cy), color=(255, 0, 0), thickness=2)

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
