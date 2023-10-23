import requests

url = "http://127.0.0.1:5000/api/detect"

# Specify the image path here
image_path = "p1.jpg"

with open(image_path, 'rb') as image_file:
    files = {
        'image': (image_path, image_file)
    }

    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response Text:", response.json())
