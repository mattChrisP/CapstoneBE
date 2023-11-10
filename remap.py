import cv2
import numpy as np


def remap_coor(x,y):
    # Define the four corners in the image
    # from the image perspective
    image_points = np.array([
        [447., 200.], # top right (origin)
        [456., 376.], # bottom right 
        [261., 373.], # bottom left
        [263., 197.], # top left
        
    ], dtype=np.float32)

    # Define the real-world coordinates of the four corners
    # Assuming the table's origin (0, 0) is the top-left corner
    real_points = np.array([
        [0, 0],       # top-right
        [0, 16],     # bottom-right
        [16, 16],  # bottom-left
        [16, 0]     # top-left
    ], dtype=np.float32)

    # Compute the homography matrix
    H, _ = cv2.findHomography(image_points, real_points)

    # Use the homography to map any image point to a real-world point
    image_point = np.array([312, 222, 1])
    real_point = np.dot(H, image_point)
    real_point = real_point / real_point[2]  # Convert to homogeneous coordinates

    x_real = real_point[0]
    y_real = real_point[1]

    print(round(x_real), round(y_real))

remap_coor(1,1)
