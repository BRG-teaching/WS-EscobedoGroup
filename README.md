# WS-EscobedoGroup

## Requirements

* [Rhino](https://www.rhino3d.com/)
* [VS Code](https://code.visualstudio.com/)
* [Anaconda3](https://www.anaconda.com/products/individual)

## Installation

To install Anaconda3, choose the appropriate iinstaller for your system [here](https://www.anaconda.com/products/individual).
During the installation process, select all default and recommended options.

Once Anaconda3 is installed, you can use `conda` (the package manager of Anaconda3) to install COMPAS on the command line.
On Windows, make sure to use Anaconda Prompt and not Command Prompt.
On Mac, you can just use Terminal.
To run the installation process, simply type:

```bash
conda config --add channels conda-forge
conda create -n workshop COMPAS --yes
```

This will create a virtual environment named "workshop" and install COMPAS and all its dependencies in it.
To test the installation, type:

```bash
conda activate workshop
python -m compas
```

You should see something similar to the following:

```text
Yay! COMPAS is installed correctly!

COMPAS: 1.1.0
Python: 3.8.2 | packaged by conda-forge | (default, Apr 24 2020, 07:56:27) [Clang 9.0.1 ]
```

## Next Steps

Once the installation is complete, you can configure VS Code and Rhino.
Instructions are available in the COMPAS documentation.

* <https://compas.dev/compas/latest/gettingstarted/vscode.html>
* <https://compas.dev/compas/latest/gettingstarted/rhino.html>

In the documentation the example environment is named "research".
Simply replace this with the name of the environment you have created during the installation process: "workshop".
