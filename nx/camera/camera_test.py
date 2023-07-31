# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 7/31/23 3:12 PM
# @File    : camera_test.py

import cv2
import time


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
    if not cap.isOpened():
        print("Failed to open camera. Exiting...")
        return

    max_fps = cap.get(cv2.CAP_PROP_FPS)
    max_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    max_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f"Max FPS: {max_fps}")
    print(f"Max Width: {max_width}")
    print(f"Max Height: {max_height}")

    frame_count = 0
    start_time = time.time()
    fps = 0

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

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
