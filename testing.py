import argparse
import time
from pathlib import Path

import cv2
import torch

from models9.common import DetectMultiBackend
from utils9.dataloaders import LoadImages
from utils9.general import (check_img_size, non_max_suppression, scale_coords, set_logging)
from utils9.torch_utils import select_device, smart_inference_mode

class ObjectDetection:
    def __init__(self, weights='yolov9-c.pt', imgsz=640, conf_thres=0.25, iou_thres=0.45):
        set_logging()
        self.device = select_device()
        self.imgsz = check_img_size(imgsz, s=32)  # YOLOv9 might use different strides; adjust as necessary
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.classes = [67]  # Index for 'cell phone'
        
        # Load model
        self.model = DetectMultiBackend(weights, device=self.device, dnn=False, data='data/coco.yaml', fp16=False)
        self.stride = self.model.stride
        self.names = self.model.names

    @smart_inference_mode()
    def detect(self, img_path, idx, camId):
        cell_phone_centers = []

        # Set Dataloader
        dataset = LoadImages(img_path, img_size=self.imgsz, stride=self.stride, auto=self.model.pt)

        # Run inference
        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            pred = self.model(img, augment=False)[0]

            # Apply NMS
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=False)

            # Process detections
            cell_phone_centers += self.process_detection(pred, path, im0s, idx, camId)

        print(f'Done. ({time.time() - t0:.3f}s)')
        return cell_phone_centers

    def process_detection(self, pred, path, im0s, idx, camId):
        cell_phone_centers = []
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im0s.shape[2:], det[:, :4], im0s.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if int(cls) == 67:  # index for "cell phone"
                        x_center = (xyxy[0] + xyxy[2]) / 2
                        y_center = (xyxy[1] + xyxy[3]) / 2
                        cv2.circle(im0s, (int(x_center), int(y_center)), 5, (0, 255, 0), -1)
                        cv2.imwrite(f"out{idx}CAM{camId}.jpg", im0s)
                        cell_phone_centers.append((int(x_center.item()), int(y_center.item())))

        return cell_phone_centers
