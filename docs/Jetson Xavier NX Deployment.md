# Jetson Xavier NX Deployment

## Flash Jetson NX:

1. Flash your Jetson NX device on a host machine with Ubuntu 18.04 or 20.04 using the NVIDIA SDK Manager. Here is [NVIDIA SDK Manager Tutorial](https://www.youtube.com/watch?v=Ucg5Zqm9ZMk&t=7s).

2. Select JetPack 5.1.1 during the installation process. This package includes specialized CUDA, cuDNN, and TensorRT versions tailored for Jetson devices. **Avoid modifying the native environment, as the specialized components may differ from standard releases.**

3. Note: The native Python 3 version in this environment is 3.8.



## Install TensorRT Library:

1. After flashing, execute the following command to install the necessary TensorRT library: `sudo apt install python3-libnvinfer*`.

2. However, `import tensorrt` within a virtual environment still not be solved yet. [How to import tensorrt in python on jetson nx](https://forums.developer.nvidia.com/t/how-to-import-tensorrt-in-python-on-jetson-nx/261353).



## Install PyTorch and TorchVision:

1. Download the appropriate PyTorch and TorchVision versions compatible with Jetson NX from this forum thread.

2. For TorchVision, follow the provided instructions to build it before use. You can find at here [PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048).



## Configure GitHub SSH:

1. Set up SSH for GitHub on your Jetson NX device by following the official GitHub guide [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).



## Install ONNX Library:

1. Refer to this forum post and reply for guidance [Installing ONNX library on my Jetson Xavier](https://forums.developer.nvidia.com/t/installing-onnx-library-on-my-jetson-xavier/115229).



## Install TensorRT on Fedora:

1. When installing TensorRT on x86 Fedora, it's recommended to use the tar package instead of RPM. This allows manual linking to Python.

2. After installation, you might need to add the following command to your `~/.bashrc` file to set the LD_LIBRARY_PATH:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/Username/Downloads/TensorRT-8.6.1.6/lib.
```

3. Keep in mind that since it's a dynamic link, you might need to execute this command in each new terminal session or add it to your system's startup scripts.



## Notice

1. If you have any questions, please check [Nvidia Developer Forum](https://forums.developer.nvidia.com/) at first!