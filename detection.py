import argparse
import time
from pathlib import Path

import cv2
import torch

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, \
    scale_coords,  set_logging

from utils.torch_utils import select_device

class ObjectDetection:

    def __init__(self):

        set_logging()
        self.device = select_device()

        # Load model
        self.model = attempt_load("yolov7.pt", map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())
        self.imgsz = check_img_size(640, s=self.stride)


    def detect(self, img_path):

        cell_phone_centers = []

        # Set Dataloader
        dataset = LoadImages(img_path, img_size=self.imgsz, stride=self.stride)

        # Get names and colors
        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names

        # Run inference
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once
        old_img_w = old_img_h = self.imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if self.device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    self.model(img, augment=False)[0]

            # Inference
            with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
                pred = self.model(img, augment=False)[0]
            # Apply NMS
            pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)


            # Process detections
            cell_phone_centers += self.process_detection(pred, path, im0s, dataset, names, img)
        print(f'Done. ({time.time() - t0:.3f}s)')
        return cell_phone_centers

    def process_detection(self, pred, path, im0s, dataset, names, img):
        cell_phone_centers = []
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if int(cls) == 67:  # index for "cell phone"
                        x_center = (xyxy[0] + xyxy[2]) / 2
                        y_center = (xyxy[1] + xyxy[3]) / 2
                        cv2.circle(im0, (int(x_center), int(y_center)), 5, (0, 255, 0), -1)
                        cv2.imwrite("out.jpg",im0)
                        cell_phone_centers.append((int(x_center.item()), int(y_center.item())))

                        x1, y1, x2, y2 = map(int, xyxy)
                        print(f"Bounding Box Coordinates for cell phone: (x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2})")
        return cell_phone_centers
