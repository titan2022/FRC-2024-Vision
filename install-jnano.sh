#!/bin/bash

# Basic dependencies
sudo apt update
sudo apt -y install libopenblas-base libopenmpi-dev libomp-dev python3.8-venv python3.8-dev libjpeg-dev zlib1g-dev python3.8

# Install OpenCV
wget https://github.com/ethanc8/titanian-repo/raw/master/debian/pool/main/o/opencv/libopencv-titanian_4.8.1-1+jnano-1_arm64.deb
sudo apt install ./libopencv-titanian_4.8.1-1+jnano-1_arm64.deb

# Create a virtual environment
mkdir -p ~/.venvs
python3.8 -m venv ~/.venvs/FRC-2024-Vision
source ~/.venvs/FRC-2024-Vision/bin/activate
# For some reason wheel is not preinstalled
python3 -m pip install wheel

# Build OpenCV


# Install PyTorch into the venv
# Older binaries are available at https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
# We can't get newer binaries as that would require a newer Python
wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
# NumPy requires Cython>=0.29.21,<3.0
python3 -m pip install "Cython>=0.29.21,<3.0"
python3 -m pip install numpy ./torch-1.10.0-cp36-cp36m-linux_aarch64.whl

# Build and install torchvision
git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
cd torchvision
python3 -m pip install build "setuptools>=40.8.0"
MAX_JOBS=3 python3 -m build --wheel --no-isolation
# The wheel will be in dist/

python3 -m pip install ./dist/torchvision-*.whl

# Install ultralytics
