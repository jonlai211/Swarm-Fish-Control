# Swarm-Fish-Control
[中文](docs/README_zh.md)

## Description

Swarm-Fish-Control is a deep learning-based project that aims to control the motion of a fish swarm by training a neural network model to control a 10x10 array of air pumps' nozzles, which emit bubbles to influence the fish swarm's behavior. 

The project consists of the following main components:

- [x] **Serial Control Code**: A set of code snippets that demonstrate how to control the air pump nozzles through serial communication by sending bytes.

- [x] **Camera Detection**: Code for detecting and interacting with a camera on Jetson NX to capture images or video streams.

- [x] **YOLO Inference with TensorRT**: A complete set of scripts for using YOLO (You Only Look Once) with TensorRT to perform real-time object detection on the captured images or video streams.

- [x] **[Jetson Xavier NX Guide](docs/Jetson%20Xavier%20NX%20Deployment.md)**: A detailed guide explaining how to deploy the project on Jetson Xavier NX and troubleshoot common errors.

- [ ] **Fish Data-Driven Training for New Detect Model**: One of the ongoing developments is the utilization of real-world fish swarm data to train and generate new recognition models. 

- [ ] **Reinforcement Learning for Adaptive Control**: Another aspect under progress is the application of reinforcement learning to achieve adaptive control of the fish swarm. 

This project serves as a preparatory step for future research in using swarm control techniques for real-world applications, such as controlling swarms of drones or autonomous boats.



## Structure
```
Swarm-Fish-Control
├── nx
│   ├── camera
│   │   ├── camera_test.py
│   │   └── camera_tracker.py
│   └── models
│       └── yolov8n.pt
├── pump
│   ├── command.py
│   ├── main.py
│   ├── system.py
│   ├── tcp_client.py
│   └── tcp_server.py
├── yolo2trt
│   ├── data
│   │   ├── bus.jpg
│   │   └── zidane.jpg
│   ├── engine_tools
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── torch_utils.py
│   │   └── utils.py
│   ├── models
│   │   └── yolov8n.engine
│   ├── outputs
│   │   ├── bus.jpg
│   │   └── zidane.jph
│   ├── config.py
│   └── infer.py
└── README.md
```



## Deployment

To deploy the Swarm-Fish-Control project, follow the steps below:

1. **Clone the repository or download the ZIP package:**
```bash
git clone git@github.com:jonlai211/Swarm-Fish-Control.git
```

2. **Navigate to the project directory:**
```bash
cd Swarm-Fish-Control
```

3. **Using Serial Communication to Control Pump:**

Modify the server parameter in `tcp_client.py` with appropriate serial port details, and run the program to start the server. The `tcp_client.py` will prompt for commands to control the air pump. For example:

`pump 1 1 1` will activate the air pump at position (1, 1) on the 10x10 air pump array.

`pump 1 1 0` will deactivate the air pump at the same position.

Alternatively, you can modify the code in `tcp_client.py` to implement custom logic for traversing all the pumps.

4. **Using Jetson NX for Visual Recognition:**
- Preparations:
    - Recompile the ONNX model into a TensorRT compatible format using the command:
    ```bash
    /usr/src/tensorrt/bin/trtexec --onnx=xxx.onnx saveEngine=xxx.engine
    ```
    - Once you have set up the correct environment, place the TensorRT engine model in the directory `yolo2trt/models/`.
    - Determine the video capture ID of the connected camera on the Jetson NX (e.g., USB0 corresponds to video capture ID 0) and modify `infer.py` accordingly:`cap = cv2.VideoCapture(0)`.
- Execution:
    - To perform real-time inference using the camera, run the following command in the terminal:
    ```bash
    python3 yolo2trt/infer.py --video --engine yolo2trt/models/yolov8n.engine
    ```
    - To perform inference on images in the directory yolo2trt/data/ and save the results in `yolo2trt/outputs/`, use the following command:
    ```bash
    python3 yolo2trt/infer.py --imgs --engine yolo2trt/models/yolov8n.engine
    ```
With these steps, you can now effectively deploy the Swarm-Fish-Control project, enabling real-time control of fish swarm behavior through the air pump array and efficient visual recognition using the Jetson Xavier NX platform.



## Tested Platforms:
- **Fedora 38**:
    - Host: XPS 15 9500
    - Kernel: 6.4.6-200.fc38.x86_64
    - GPU: NVIDIA GeForce GTX 1650 Ti Mobile
    - CUDA: 11.7
    - TensorRT: 8.6.1


- **Jetson Xavier NX**:
    - OS: Ubuntu 20.04.6 LTS aarch64
    - Host: NVIDIA Jetson Xavier NX Developer Kit
    - Kernel: 5.10.104-tegra
    - Jetpack: 5.1.1


## Optimizations

In this project, several optimizations have been introduced to enhance performance and user experience in part of YOLO to TensorRT.

1. YOLO Real-time Inference with TensorRT
One significant improvement is the integration of YOLO (You Only Look Once) with TensorRT for real-time object detection. By leveraging TensorRT's high-performance deep learning inference capabilities, the project achieves faster and more efficient detection on the captured camera frames or video streams.

2. Simplified Command-Line Interface
The command-line interface (CLI) has been streamlined to make it more user-friendly. With simplified command options, users can now easily specify the input source (`--video` or `--imgs`) and control whether to display the detection results interactively (`--show`).


## Acknowledgements

 - [YOLOv8-TensorRT](https://github.com/triple-Mu/YOLOv8-TensorRT)
 - [Ultralytics](https://github.com/ultralytics/ultralytics)