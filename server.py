from flask import Flask, request, jsonify
import cv2
import numpy as np
import torch
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords

app = Flask(__name__)

# Load model once during server start-up to avoid repeated loading
model = attempt_load('yolov7-tiny.pt', map_location=torch.device('cpu'))
img_size = 640

def process_detections(pred, im0s):
    cell_phone_centers = []
    for i, det in enumerate(pred):
        if len(det):
            im0 = im0s.copy()
            det[:, :4] = scale_coords((img_size, img_size), det[:, :4], im0.shape).round()

            for *xyxy, _, cls in reversed(det):
                if int(cls) == 67:  # "cell phone"
                    x_center = (xyxy[0] + xyxy[2]) / 2
                    y_center = (xyxy[1] + xyxy[3]) / 2
                    cv2.circle(im0, (int(x_center), int(y_center)), 5, (0, 255, 0), -1)
                    cell_phone_centers.append((x_center.item(), y_center.item()))
                    x1, y1, x2, y2 = map(int, xyxy)
                    print(f"Bounding Box for cell phone: x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")

    return cell_phone_centers

@app.route("/detect", methods=["POST"])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    im0s = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

    # Padded resize
    img = letterbox(im0s, img_size, stride=32)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).float() / 255.0  # Convert to tensor

    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img)[0]
    pred = non_max_suppression(pred, 0.25, 0.45)
    cell_phone_centers = process_detections(pred, im0s)

    return jsonify({"cell_phone_centers": cell_phone_centers})


if __name__ == '__main__':
    app.run()
