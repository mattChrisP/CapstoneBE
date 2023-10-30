
import cv2
import numpy as np
import torch
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords

class ObjectDetection:

    def __init__(self):
        # Load model once during server start-up to avoid repeated loading
        self.model = attempt_load('yolov7-tiny.pt', map_location=torch.device('cpu'))
        self.img_size = 640

    def detect(self, image):

        # TODO: get the img use other func
        im0s = cv2.imread(image)

        if im0s is None:
            print(f"Image at {image} could not be loaded.")

        # Padded resize
        img = letterbox(im0s, self.img_size, stride=32)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).float() / 255.0  # Convert to tensor

        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = self.model(img)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)
        cell_phone_centers = self.process_detections(pred, im0s)

        return {"cell_phone_centers": cell_phone_centers}



    def process_detections(self, pred, im0s):
        cell_phone_centers = []
        for i, det in enumerate(pred):
            if len(det):
                im0 = im0s.copy()
                det[:, :4] = scale_coords((self.img_size, self.img_size), det[:, :4], im0.shape).round()

                for *xyxy, _, cls in reversed(det):
                    if int(cls) == 67:  # "cell phone"
                        x_center = (xyxy[0] + xyxy[2]) / 2
                        y_center = (xyxy[1] + xyxy[3]) / 2
                        cv2.circle(im0, (int(x_center), int(y_center)), 5, (0, 255, 0), -1)
                        cell_phone_centers.append((x_center.item(), y_center.item()))
                        x1, y1, x2, y2 = map(int, xyxy)
                        print(f"Bounding Box for cell phone: x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")

        return cell_phone_centers