import time
import cv2

from detection import ObjectDetection
from camera import BUFFER, get_image
# from camera import get_image

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
    get_image()
    img_path = f"obj{idx}.jpg"
    image = cv2.imread(img_path)

    res = ins.detect(image=img_path)
    coord = res.get("cell_phone_centers", None)
    if coord:
        cv2.circle(image, (coord[0], coord[1]), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.imwrite(img_path, image)

    print(res)
    time.sleep(5)
    cnt += 1

    
