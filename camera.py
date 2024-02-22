import os

BUFFER = 1
img_idx = 0


def get_image(camera_device, id):
    global img_idx
    img_idx += 1
    if img_idx == BUFFER+1:
        img_idx = 1

    os.system(f"fswebcam -d {camera_device} -r 640x640 --no-banner obj{img_idx}cam{id}.jpg")
    # os.system(f"convert obj{img_idx}cam{id}.jpg -resize 640x640^ -gravity center -crop 640x640+0+0 +repage obj{img_idx}cam{id}.jpg")
    



# Example usage
# camera_device = "/dev/video0"  # Change this based on your camera (use /dev/video1 for the other camera)