# Swarm-Fish-Control

## 项目描述

Swarm-Fish-Control是一个基于深度学习的项目，旨在通过训练神经网络模型来控制一个10x10的气泵阵列的喷嘴，通过喷射气泡来影响鱼群的运动。

该项目包括以下主要组件：

-[x] **串口控制代码**： 一组代码片段，演示如何通过串口通信来控制气泵喷嘴，通过发送字节实现控制。

-[x] **摄像头检测**: 用于检测和与Jetson NX上的摄像头交互，捕获图像或视频流。

-[x] **使用TensorRT的YOLO推理**: 一套完整的脚本，用于在捕获的图像或视频流上使用YOLO（You Only Look Once）与TensorRT进行实时目标检测。

-[x] **Jetson Xavier NX指南**: 详细说明如何在Jetson Xavier NX上部署项目并解决常见问题。

-[ ] **基于鱼群数据的新检测模型训练**: 正在进行的一项发展是利用真实世界的鱼群数据来训练和生成新的识别模型。

-[ ] **自适应控制的强化学习**: 另一个正在进行的令人兴奋的方面是应用强化学习实现对鱼群的自适应控制。

该项目为未来研究使用群控技术在实际应用中（例如控制无人机或自动船的群体运动）做准备。


## 文件目录
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



## 部署

要部署Swarm-Fish-Control项目，请按照以下步骤操作：

1. **克隆或下载ZIP包:**
```bash
git clone git@github.com:jonlai211/Swarm-Fish-Control.git
```

2. **进入项目目录:**
```bash
cd Swarm-Fish-Control
```

3. **使用串口通信控制气泵:**

修改 `tcp_client.py` 中的server参数以匹配正确的串口信息，并运行程序开启服务器。 `tcp_client.py` 会提示输入命令以控制气泵。例如：

`pump 1 1 1` 将激活10x10气泵台上位置（1, 1）的气泵。

`pump 1 1 0` 将关闭同一位置的气泵。

或者，您还可以在 `tcp_client.py` 中修改代码以实现遍历所有气泵的自定义逻辑。

4. **在Jetson NX上进行视觉识别:**
- 执行:
    - 使用以下命令将ONNX模型重新编译为TensorRT兼容格式：
    ```bash
    /usr/src/tensorrt/bin/trtexec --onnx=xxx.onnx saveEngine=xxx.engine
    ```
    - 安装正确的环境后，将TensorRT engine模型放置在目录 `yolo2trt/models/`中。
    - 确定Jetson NX上连接的摄像头的视频捕获ID（例如USB0对应视频捕获ID 0），并相应地修改 `infer.py` 中的 `cap = cv2.VideoCapture(0)`.
- Execution:
    - 要使用摄像头进行实时推理，请在终端中运行以下命令：
    ```bash
    python3 yolo2trt/infer.py --video --engine yolo2trt/models/yolov8n.engine
    ```
    - 要对目录 `yolo2trt/data/` 中的图像进行推理并将结果保存在 `yolo2trt/outputs/`中，请使用以下命令：
    ```bash
    python3 yolo2trt/infer.py --imgs --engine yolo2trt/models/yolov8n.engine
    ```
通过上述步骤，您现在可以有效地部署Swarm-Fish-Control项目，实现通过气泵阵列实时控制鱼群行为，并在Jetson Xavier NX平台上进行高效的视觉识别。


## 测试平台:
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


## 优化

在该项目中，引入了一些优化措施，以提高YOLO到TensorRT部分的功能和用户体验。

1. YOLO实时推理与TensorRT集成
一个重要的改进是将YOLO与TensorRT集成，以实现实时目标检测。通过利用TensorRT的高性能深度学习推理能力，该项目在捕获的摄像头帧或视频流上实现更快、更高效的检测。
2. 简化命令行界面
优化了命令行界面（CLI），使其更加用户友好。通过简化命令选项，用户现在可以轻松地指定输入源（`--video`或`--imgs`），并控制是否交互式显示检测结果（`--show`）。

## 致谢

- [YOLOv8-TensorRT](https://github.com/triple-Mu/YOLOv8-TensorRT)
- [Ultralytics](https://github.com/ultralytics/ultralytics)