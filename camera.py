import os

BUFFER = 1
img_idx = 0


def get_image(camera_device, id):
    global img_idx
    img_idx += 1
    if img_idx == BUFFER+1:
        img_idx = 1

    os.system(f"fswebcam -d {camera_device} -r 800x600 --no-banner obj{img_idx}cam{id}.jpg")


# Example usage
# camera_device = "/dev/video0"  # Change this based on your camera (use /dev/video1 for the other camera)