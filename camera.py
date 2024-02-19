import os

BUFFER = 5
img_idx = 0


def get_image(camera_device):
    global img_idx
    img_idx += 1
    if img_idx == BUFFER+1:
        img_idx = 1

    os.system(f"fswebcam -d /dev/video0 -r 1280x720 --no-banner test.jpg")


# Example usage
# camera_device = "/dev/video0"  # Change this based on your camera (use /dev/video1 for the other camera)