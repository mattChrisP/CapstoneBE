import time
import cv2

from detection import ObjectDetection
from camera import BUFFER, get_image
ins = ObjectDetection()
cnt = 0

idx = 0
while True:
    idx += 1
    if idx == BUFFER + 1:
        idx = 1

    # This is for testing only, remove the cnt for prod
    if cnt == 1:
        break
    
    # get_image()
    img_path = f"obj{3}.jpg"
    image = cv2.imread(img_path)

    res = ins.detect(img_path)

    # Mapping the center of phone coordinate back to image
    print(res)
    time.sleep(5)
    cnt += 1
