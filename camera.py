import os

BUFFER = 5
img_idx = 0


def get_image():
    global img_idx
    img_idx += 1
    if img_idx == BUFFER+1:
        img_idx = 1

    os.system(f"libcamera-still -o obj{img_idx}.jpg --width 640 --height 640 --rotation 180")
    