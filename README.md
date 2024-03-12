# FRC-2024-Vision
Coprocessor code for 2024

## Cloning this repo

This repository uses Git LFS.

First, install Git LFS:

```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install git-lfs
git lfs install
```

Next, clone the repo:

```bash
git clone https://github.com/titan2022/FRC-2024-Vision
```

## Running the code

First install the dependencies (as listed below), and build Titan-Processing in `../Titan-Processing`. Then, you can do:

```bash
cd src
python3 example-webcam.py
```

## Autostart (Jetson Nano)

First, please go into the Unity network settings, click "Edit Connections...", and for each network connection, edit the connection and select "General->All users may connect to this network".

Next, go into this directory and run `./autostart-jnano.sh` and reboot. To return to the desktop, run `./no-autostart-jnano.sh` and reboot.

To see the status, run `systemctl status titan2022`. To see the full logs, run `journalctl -u titan2022 -b`. To follow the logs, run `journalctl -u titan2022 -f`. To stop the service, run `sudo systemctl stop titan2022`.

## Install dependencies

### Jetson Nano installation

On a stock JetPack 4.6.1 / Ubuntu 18.04 installation, run:

```bash
wget -qO- https://raw.githubusercontent.com/titan2022/FRC-2024-Vision/main/setup-jnano.sh | bash
```

### Install conda/miniforge

First, please have Conda installed on your computer. If it's not installed, please install [Miniforge3](https://conda-forge.org/miniforge/), which includes Conda and a conda-forge based Python environment. You can install Miniforge3 using the following command:

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
rm Miniforge3-$(uname)-$(uname -m).sh
```

Close and reopen your shell, and run:

```bash
# Prevent Conda from polluting your environment when you're not working on Conda-managed projects.
conda config --set auto_activate_base false
```

### Install dependencies with Conda

Now, you can use Conda to install the dependencies.

```bash
conda env create -f environment-cpu.yml # or -cuda -intel -jnano
conda activate FRC-2024-Vision
```

(This might not be necessary) Install a OpenCL implementation.
* If you already have an OpenCL implementation, `conda install ocl-icd-system`
* On the Jetson Nano:
  * TODO
* On any system with CUDA, `conda install pocl-cuda`
* On an Intel GPU, `conda install intel-compute-runtime`

If you modify `environment.yml`, please run

```bash
conda env update -f environment-cpu.yml
```