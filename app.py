import time

from detection import ObjectDetection
# from camera import get_image

ins = ObjectDetection()

while True:
    img_path = "p1.jpg"

    res = ins.detect(image=img_path)
    print(res)
    time.sleep(5)

    
