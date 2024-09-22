import cv2
import numpy as np

# Load the image
image = cv2.imread('blood_splatter.jpg')

# Create copies of the original image for different windows
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

        # Draw a small green circle at the center of each bloodstain (satellite points) on both images
        cv2.circle(image_with_satellite_points, (cx, cy), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(image_with_lines, (cx, cy), radius=5, color=(0, 255, 0), thickness=-1)

        # Label the stains for easy identification (main vs satellite)
        cv2.putText(image_with_satellite_points, f"{i+1}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image_with_lines, f"{i+1}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# OPTIONAL: Draw lines between the main bloodstain and its satellite stains on the "image_with_lines"
# Assumption: The largest contour is the main bloodstain, and the others are satellite stains
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

# Display the results in three separate windows
cv2.imshow('Satellite Points Only', image_with_satellite_points)  # Window with satellite points, no lines
cv2.imshow('Satellite Points with Blue Lines', image_with_lines)  # Window with points and blue lines
cv2.imshow('Original Blood Splatter', image_original)             # Window with the original image only

# Wait for the user to press a key
cv2.waitKey(0)
cv2.destroyAllWindows()
