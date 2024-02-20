import cv2
import numpy as np

# Lists to store the points
points = []
complete = False

def select_point(event, x, y, flags, param):
    global points, image, complete

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", image)
        points.append([x, y])

        if len(points) == 4:
            complete = True

# Load the image
image = cv2.imread('obj1cam1.jpg')
if image is None:
    print("Failed to load image")
    exit()

cv2.imshow("Image", image)
cv2.setMouseCallback("Image", select_point)

while not complete:
    cv2.waitKey(1)

cv2.destroyAllWindows()
image_points = np.array(points, dtype=np.float32)
print(image_points)
