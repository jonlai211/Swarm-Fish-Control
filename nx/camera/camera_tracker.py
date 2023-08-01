# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 8/1/23 9:47 AM
# @File    : camera_tracker.py

import cv2
import time
from ultralytics import YOLO


def calculate_fps(frame_count, start_time):
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time >= 1.0:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = current_time
    else:
        fps = None

    return fps, frame_count, start_time


def main():
    cap = cv2.VideoCapture(4)
    model = YOLO("../models/yolov8n.pt")

    boxes = []
    ids = None
    frame_count = 0
    start_time = time.time()
    fps = 0

    if not cap.isOpened():
        print("Failed to open camera. Exiting...")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame stream. Exiting...")
            break

        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = current_time
        if fps != 0:
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        results = model.track(frame, persist=True)
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
        else:
            print("No objects detected in this frame.")
        for box, id in zip(boxes, ids):
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"Id {id}",
                (box[0], box[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
