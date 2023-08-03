# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 8/3/23 10:43 AM
# @File    : infer.py

import argparse
import torch
import cv2
import time

from config import CLASSES, COLORS
from engine_tools import TRTModule
from engine_tools.torch_utils import det_postprocess
from engine_tools.utils import blob, letterbox, path_to_list
from pathlib import Path


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine',
                        type=str,
                        help='Engine file')
    parser.add_argument('--video',
                        action='store_true',
                        help='Use video input')
    parser.add_argument('--imgs',
                        action='store_true',
                        help='Use images input')
    parser.add_argument('--show',
                        action='store_true',
                        help='Show the detection results')
    parser.add_argument('--out-dir',
                        type=str,
                        default='yolo2trt/outputs',
                        help='Path to output file')
    parser.add_argument('--device',
                        type=str,
                        default='cuda:0',
                        help='TensorRT infer device')
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace) -> None:
    device = torch.device(args.device)
    engine = TRTModule(args.engine, device)
    save_path = Path(args.out_dir)

    H, W = engine.inp_info[0].shape[-2:]

    # set desired output names order
    engine.set_desired(['num_dets', 'bboxes', 'scores', 'labels'])

    if not args.show and not save_path.exists():
        save_path.mkdir(parents=True, exist_ok=True)

    if args.video:
        frame_count = 0
        start_time = time.time()
        fps = 0
        cap = cv2.VideoCapture(4)

        while True:
            ret, frame = cap.read()
            if not ret:
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

            bgr = frame.copy()
            bgr, ratio, dwdh = letterbox(bgr, (W, H))
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            tensor = blob(rgb, return_seg=False)
            dwdh = torch.asarray(dwdh * 2, dtype=torch.float32, device=device)
            tensor = torch.asarray(tensor, device=device)
            # inference
            data = engine(tensor)

            bboxes, scores, labels = det_postprocess(data)
            if bboxes.numel() == 0:
                # if no bounding box
                print('No objects detected in this frame.')
                continue
            bboxes -= dwdh
            bboxes /= ratio

            for (bbox, score, label) in zip(bboxes, scores, labels):
                bbox = bbox.round().int().tolist()
                cls_id = int(label)
                cls = CLASSES[cls_id]
                color = COLORS[cls]
                cv2.rectangle(frame, bbox[:2], bbox[2:], color, 2)
                cv2.putText(frame,
                            f'{cls}:{score:.3f}', (bbox[0], bbox[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, [225, 255, 255],
                            thickness=2)

            cv2.imshow('result', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    if args.imgs:
        images = path_to_list('yolo2trt/data')

        for image in images:
            save_image = save_path / image.name
            bgr = cv2.imread(str(image))
            draw = bgr.copy()
            bgr, ratio, dwdh = letterbox(bgr, (W, H))
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            tensor = blob(rgb, return_seg=False)
            dwdh = torch.asarray(dwdh * 2, dtype=torch.float32, device=device)
            tensor = torch.asarray(tensor, device=device)
            # inference
            data = engine(tensor)

            bboxes, scores, labels = det_postprocess(data)
            if bboxes.numel() == 0:
                # if no bounding box
                print(f'{image}: no object!')
                continue
            bboxes -= dwdh
            bboxes /= ratio

            for (bbox, score, label) in zip(bboxes, scores, labels):
                bbox = bbox.round().int().tolist()
                cls_id = int(label)
                cls = CLASSES[cls_id]
                color = COLORS[cls]
                cv2.rectangle(draw, bbox[:2], bbox[2:], color, 2)
                cv2.putText(draw,
                            f'{cls}:{score:.3f}', (bbox[0], bbox[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, [225, 255, 255],
                            thickness=2)

            cv2.imwrite(str(save_image), draw)


if __name__ == '__main__':
    args = parse_args()
    main(args)
