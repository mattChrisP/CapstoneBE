import os

BUFFER = 5
img_idx = 0


def get_image(camera_device):
    global img_idx
    img_idx += 1
    if img_idx == BUFFER+1:
        img_idx = 1

    os.system(f"libcamera-still -o obj{img_idx}CAM{camera_device}.jpg --width 640 --height 640 --rotation 180 --timeout 1 --nopreview --device {camera_device}")
    

# Example usage
# camera_device = "/dev/video0"  # Change this based on your camera (use /dev/video1 for the other camera)