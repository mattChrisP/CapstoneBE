import cv2
import numpy as np

# Define the four corners in the image
image_points = np.array([
    [ 619., 1106.],
    [ 227., 242.],
    [ 686., 146.],
    [1246., 773.],
    
], dtype=np.float32)

# Define the real-world coordinates of the four corners
# Assuming the table's origin (0, 0) is the top-left corner
real_points = np.array([
    [0, 0],       # top-left
    [126, 0],     # top-right
    [126, 67.5],  # bottom-right
    [0, 67.5]     # bottom-left
], dtype=np.float32)

# Compute the homography matrix
H, _ = cv2.findHomography(image_points, real_points)

# Use the homography to map any image point to a real-world point
image_point = np.array([650.5, 325.5, 1])
real_point = np.dot(H, image_point)
real_point = real_point / real_point[2]  # Convert to homogeneous coordinates

x_real = real_point[0]
y_real = real_point[1]

print(x_real, y_real)
