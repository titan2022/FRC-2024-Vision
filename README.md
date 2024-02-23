# FRC-2024-Vision
Coprocessor code for 2024

## Install dependencies

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
conda env create -f environment.yml
conda activate FRC-2024-Vision
```

If you modify `environment.yml`, please run

```bash
conda env update -f environment.yml
```