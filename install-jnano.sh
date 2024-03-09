#!/bin/bash

# Basic dependencies
sudo add-apt-repository universe
sudo apt update
sudo apt -y install libopenblas-base libopenmpi-dev libomp-dev python3.8-venv python3.8-dev libjpeg-dev zlib1g-dev libopenmpi3 python3.8

# Create a virtual environment
mkdir -p ~/.venvs
python3.8 -m venv ~/.venvs/FRC-2024-Vision
source ~/.venvs/FRC-2024-Vision/bin/activate
# For some reason wheel is not preinstalled
pip install wheel
pip install --upgrade pip

# # Build OpenCV
# sudo apt -y install build-essential cmake git unzip pkg-config zlib1g-dev libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libglew-dev libgtk2.0-dev libgtk-3-dev libcanberra-gtk* python3-dev python3-numpy python3-pip libxvidcore-dev libx264-dev libgtk-3-dev libtbb2 libtbb-dev libdc1394-22-dev libxine2-dev gstreamer1.0-tools libv4l-dev v4l-utils qv4l2  libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libavresample-dev libvorbis-dev libxine2-dev libtesseract-dev libfaac-dev libmp3lame-dev libtheora-dev libpostproc-dev libopencore-amrnb-dev libopencore-amrwb-dev libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev liblapacke-dev libeigen3-dev gfortran libhdf5-dev protobuf-compiler libprotobuf-dev libgoogle-glog-dev libgflags-dev
# export CMAKE_ARGS="-D WITH_OPENCL=OFF -D WITH_CUDA=ON -D CUDA_ARCH_BIN=5.3 -D CUDA_ARCH_PTX="" -D WITH_CUDNN=ON -D WITH_CUBLAS=ON -D ENABLE_FAST_MATH=ON -D CUDA_FAST_MATH=ON -D OPENCV_DNN_CUDA=ON-D ENABLE_NEON=ON -D WITH_QT=OFF -D WITH_OPENMP=ON -D BUILD_TIFF=ON -D WITH_FFMPEG=ON -D WITH_GSTREAMER=ON -D WITH_TBB=ON -D BUILD_TBB=ON -D BUILD_TESTS=OFF -D WITH_EIGEN=ON -D WITH_V4L=ON -D WITH_LIBV4L=ON -D WITH_PROTOBUF=ON -D OPENCV_ENABLE_NONFREE=ON -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=OFF -D OPENCV_GENERATE_PKGCONFIG=ON -D BUILD_EXAMPLES=OFF"
# git clone --recursive https://github.com/opencv/opencv-python.git
# cd opencv-python 
# export ENABLE_CONTRIB=1
# pip wheel . --verbose

wget https://github.com/ethanc8/titanian-repo/releases/download/opencv-4.9.0-jnano-py38/opencv_contrib_python-4.9.0.80-cp38-cp38-linux_aarch64.whl
pip install ./opencv_contrib_python-4.9.0.80-cp38-cp38-linux_aarch64.whl

# Build PyTorch
sudo apt install ninja-build git cmake libjpeg-dev libopenmpi-dev libomp-dev ccache libopenblas-dev libblas-dev libeigen3-dev clang-8
pip install mock pillow testresources setuptools==58.3.0 scikit-build
pip install --upgrade protobuf
git clone -b titanian-erista --depth=1 --recursive https://github.com/ethanc8/pytorch.git
cd pytorch
pip install -r requirements.txt
sudo ln -s /usr/lib/aarch64-linux-gnu/libcublas.so /usr/local/cuda/lib64/libcublas.so
export BUILD_CAFFE2_OPS=OFF
export USE_FBGEMM=OFF
export USE_FAKELOWP=OFF
export BUILD_TEST=OFF
export USE_MKLDNN=OFF
export USE_NNPACK=OFF
export USE_XNNPACK=OFF
export USE_QNNPACK=OFF
export USE_PYTORCH_QNNPACK=OFF
export USE_CUDA=ON
export USE_CUDNN=ON
export TORCH_CUDA_ARCH_LIST="5.3;6.2;7.2"
export USE_NCCL=OFF
export USE_SYSTEM_NCCL=OFF
export USE_OPENCV=OFF
export MAX_JOBS=4
export PATH=/usr/lib/ccache:$PATH
export CC=clang-8
export CXX=clang++-8
export CUDACXX=/usr/local/cuda/bin/nvcc
python3 setup.py clean # clean previous build if it exists
python3 setup.py bdist_wheel

# Install PyTorch into the venv
# Older binaries are available at https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
# We can't get newer binaries as that would require a newer Python
wget https://github.com/ethanc8/titanian-repo/releases/download/pytorch-1.13.0-jnano-py38/torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl -O torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl
wget https://github.com/ethanc8/titanian-repo/releases/download/pytorch-1.13.0-jnano-py38/torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl -O torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl
# NumPy requires Cython>=0.29.21,<3.0
pip install "Cython>=0.29.21,<3.0"
pip install numpy ./torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl ./torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl

# # Build and install torchvision
# git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
# cd torchvision
# python3 -m pip install build "setuptools>=40.8.0"
# MAX_JOBS=3 python3 -m build --wheel --no-isolation
# # The wheel will be in dist/
# python3 -m pip install ./dist/torchvision-*.whl

# Install ultralytics
pip install ultralytics