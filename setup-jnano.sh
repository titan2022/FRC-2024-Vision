#!/bin/bash

mkdir -p ~/Projects/titanian-download/setup && cd ~/Projects/titanian-download/setup
# Basic dependencies
sudo add-apt-repository universe
sudo apt update
sudo apt -y install libopenblas-base libopenmpi-dev libomp-dev python3.8-venv python3.8-dev libjpeg-dev zlib1g-dev libopenmpi-dev python3.8 curl wget build-essential cmake git unzip pkg-config zlib1g-dev libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libglew-dev libgtk2.0-dev libgtk-3-dev libcanberra-gtk* python3-dev python3-numpy python3-pip libxvidcore-dev libx264-dev libgtk-3-dev libtbb2 libtbb-dev libdc1394-22-dev libxine2-dev gstreamer1.0-tools libv4l-dev v4l-utils qv4l2  libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libavresample-dev libvorbis-dev libxine2-dev libtesseract-dev libfaac-dev libmp3lame-dev libtheora-dev libpostproc-dev libopencore-amrnb-dev libopencore-amrwb-dev libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev liblapacke-dev libeigen3-dev gfortran libhdf5-dev protobuf-compiler libprotobuf-dev libgoogle-glog-dev libgflags-dev

# Set up Git LFS and clone the repo
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install git-lfs
git lfs install
pushd ~/Projects
  git clone https://github.com/titan2022/FRC-2024-Vision
popd

# Create a virtual environment
mkdir -p ~/.venvs
python3.8 -m venv ~/.venvs/FRC-2024-Vision
source ~/.venvs/FRC-2024-Vision/bin/activate
# For some reason wheel is not preinstalled
pip install wheel
pip install --upgrade pip

# Install numpy
pip install "Cython>=0.29.21,<3.0"
pip install numpy

# Install opencv
wget https://github.com/ethanc8/titanian-repo/releases/download/opencv-4.9.0-jnano-py38/opencv_contrib_python-4.9.0.80-cp38-cp38-linux_aarch64.whl https://github.com/ethanc8/titanian-repo/releases/download/opencv-4.9.0-jnano-py38/opencv_python-4.9.0.80-py2.py3-none-any.whl
pip install ./opencv_contrib_python-4.9.0.80-cp38-cp38-linux_aarch64.whl ./opencv_python-4.9.0.80-py2.py3-none-any.whl

# Install PyTorch into the venv
wget https://github.com/ethanc8/titanian-repo/releases/download/pytorch-1.13.0-jnano-py38-bionic/torch-1.13.0a0+git7a7b8c9-cp38-cp38-linux_aarch64.whl https://github.com/ethanc8/titanian-repo/releases/download/pytorch-1.13.0-jnano-py38-bionic/torchvision-0.14.1a0+5e8e2f1-cp38-cp38-linux_aarch64.whl
pip install ./torch-1.13.0a0+git7a7b8c9-cp38-cp38-linux_aarch64.whl ./torchvision-0.14.1a0+5e8e2f1-cp38-cp38-linux_aarch64.whl

# Install ultralytics
pip install ultralytics dill 'lapx>=0.5.2'

# Install librealsense2
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
sudo apt install librealsense2-utils librealsense2-dev
pip install pyrealsense2

# Set up zram and reboot
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/apps/More%20RAM/install | bash
sudo reboot now