import time
import cv2

from detection import ObjectDetection
from camera import BUFFER, get_image
from remap import remap_coor


ins = ObjectDetection()
cnt = 0

idx = 0
while True:
    idx += 1
    if idx == BUFFER + 1:
        idx = 1

    # This is for testing only, remove the cnt for prod
    # if cnt == 5:
    #     break
    
    get_image()
    img_path = f"obj{idx}.jpg"
    image = cv2.imread(img_path)

    res = ins.detect(img_path, idx)


    # Mapping the center of phone coordinate back to image
    print(res)
    

    time.sleep(2)
    cnt += 1
