# Jetson Xavier NX 部署指南

## 刷写 Jetson NX：

1. 在主机上使用 Ubuntu 18.04 或 20.04 通过 NVIDIA SDK 管理器刷写您的 Jetson NX 设备。这里有 [NVIDIA SDK 管理器教程](https://www.youtube.com/watch?v=Ucg5Zqm9ZMk&t=7s).

2. 在安装过程中选择 JetPack 5.1.1。此套件包含专为 Jetson 设备定制的 CUDA、cuDNN 和 TensorRT 版本。 **避免修改本机环境，因为这些专门的组件可能与标准版本有所不同**.

3. 注意：此环境中本机 Python 3 版本为 3.8。



## 安装 TensorRT 库：

1. 刷写完成后，执行以下命令安装必要的 TensorRT 库： `sudo apt install python3-libnvinfer*`.

2. 然而，在虚拟环境内使用 `import tensorrt 仍未解决`. [如何在 Jetson NX 上的 Python 中导入 TensorRT](https://forums.developer.nvidia.com/t/how-to-import-tensorrt-in-python-on-jetson-nx/261353).



## 安装 PyTorch 和 TorchVision：:

1. 从这个论坛主题中下载与 Jetson NX 兼容的适当版本的 PyTorch 和 TorchVision.

2. 对于 TorchVision，在使用前请按照提供的说明进行构建. 你可以在这里找到[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048).



## 配置 GitHub SSH：

1. 按照官方 GitHub 指南设置 Jetson NX 设备上的 GitHub SSH. [通过 SSH 连接到 GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).



## 安装 ONNX 库：

1. 请参考这个论坛主题中的帖子和回复，以获取关于安装 ONNX 库的指导. [在 Jetson Xavier 上安装 ONNX 库](https://forums.developer.nvidia.com/t/installing-onnx-library-on-my-jetson-xavier/115229).



## 在 Fedora 上安装 TensorRT：

1. 在 x86 Fedora 上安装 TensorRT 时，推荐使用 tar 包而不是 RPM。这允许手动链接到 Python.

2. 安装完成后，您可能需要将以下命令添加到您的 ~/.bashrc 文件以设置 LD_LIBRARY_PATH：
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/Username/Downloads/TensorRT-8.6.1.6/lib.
```

3. 请注意，由于这是一个动态链接，您可能需要在每个新的终端会话中执行此命令，或将其添加到系统的启动脚本中.



## 注意事项

1. 如果您有任何问题，请首先查看 [Nvidia 开发者论坛](https://forums.developer.nvidia.com/)！