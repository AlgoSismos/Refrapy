![](src/refrapy/images/refrapy_logo.png)

Refrapy is a graphical application for seismic refraction data analysis. It is written in Python and uses 
open source libraries from numerical and geophysics python communities to 
provide a visual interface for geophycists analyse seismic refraction data.

# Installation

Before proceeding it should be advised that currently Refrapy only works with python versions from 3.9 to 3.12 and that one that one of this versions should be installed in your system. Besides that, It is also important to mention that Refrapy depends on tkinter (a wrapper around Tcl/Tk GUI framework), and although tkinter comes with python, some  distributions / operational systems consider this package is an optional python package that must be installed independently. Feel free to open an issue if you encounter any issue while installing this package.

## Stand-alone application installation

Below we provide two installation methods for using Refrapy as a stand-alone application.

### Installing Refrapy with pipx
```bash
pipx install git+https://github.com/AlgoSismos/Refrapy
```

pipx is a community open source tool for installing stand-alone python applications from Python Package Index (PYPI). It installs the application in an isolated environment and makes it available in the user space 
without affecting other environments.

For pipx installation instructions and usage see its [official documentation](https://pipx.pypa.io/stable/docs/).

### Installing Refrapy with uv

```bash
uv tool install --python-preference only-system git+https://github.com/AlgoSismos/Refrapy
```
uv is an open source python packaging tool developed by [Astral](https://astral.sh/). For instalation instructions follow the instructions on the official [uv documentation](https://docs.astral.sh/uv/).

## Virtual environment installation (not recommended)

Since Refrapy is a stand-alone application, installing it inside a virtual environment is not recommended and 
should be used only in case the previous procedures do not work, or to test the application and it's execution.
Another, very specific, use case should be when using Refrapy only as a support tool for a data analysis within a python environment, but even in this case it should be possible to install it as a stand-alone application and call it inside the environment as any regular program in your computer.

Below we indicate a two methods for installing Refrapy inside a virtual environment, using pip+venv and uv. In all this cases you must (inside a terminal) create a new folder for the project and move inside this directory.

### Installing Refrapy with pip/env

For installing Refrapy inside a virtual environment you must first create it in a folder, by running in your terminal:
```bash
python -m venv env_name
```
where `env_name` is the name of the folder containing your environment.

Different procedures are used to activate your environment on Linux and Mac or on Windows. To activate your environment on Linux or Mac, run:
```bash
source env_name/bin/activate
```

on Windows Powershell run:
```bash
env_name\Scripts\Activate.ps1
```
and if you receive an error message it [*may* be necessary](https://docs.python.org/3/library/venv.html) to run the following command on your terminal before activating the virtual environment you just created:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

A list of activation scripts can be found on python's [official documentation](https://docs.python.org/3/library/venv.html).

After this you just need to install the package using:
```bash
pip install git+https://github.com/AlgoSismos/Refrapy
```
and do not forget to run `deactivate` when you are done with your work in this environment.

<!-- ### Installing Refrapy with uv (and creating a virtual environment) -->


<!-- ### Installing Refrapy using conda

THE DESCRIPTION BELOW IS OUTDATED:

It is recommended the use of Anaconda (https://www.anaconda.com/), because it simplifies package management.
Once it is installed, run the following commands on the Anaconda prompt (**tested on Windows 10 system, with Python 3.8.13**):

   ```
   conda create -n refrapy python=3.8
   conda activate refrapy
   conda install obspy
   conda install -c gimli -c conda-forge pygimli
   pip install pmw
   ```
    
Once all the necessary packages are installed, extract Refrapick.py, Refrainv.py and the images folder to a directory on your computer. Sample data are also available for download.

You can execute the Python files by running:

   ```
   python Refrapick.py
   python Refrainv.py 
   ``` -->

## Using Refrapy

There are two applications bundled with Refrapy, Refrapick and Refrainv. 

### Refrapick

The Refrapick program is used for basic waveform processing and for first breaks picking. The software is aimed to work mainly around SEG2 files, but all waveform formats readable by [ObsPy](https://www.obspy.org/) can be used. However, there are a few conditions that need to be considered when reading multichannel waveform data. Waveform **files with missing data traces cannot be used as input**, which can occur with files that have already passed through some other processing software, where one or more traces were removed manually, probably due to being bad noisy data. Thus, **it is recommended the use of original files (i.e., without any editing)**. Also, receivers and source position may not be well defined in the file header or may fail to be properly read. **In such cases, instead of obtaining this information automatically (conventional attempt), dialog boxes appear so that the user can enter these required values**.

For calling Refrapick, on your terminal, call:
```bash
refrapy pick
```
For usage, follow the instructions on the video below:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/3a9eZW4WKjI/0.jpg)](https://www.youtube.com/watch?v=3a9eZW4WKjI)


### Refrainv

The Refrainv program is used to run a time-terms and a traveltimes tomography inversion. The latter is powered by pyGIMLi (https://www.pygimli.org/). The program presents an individual frame for each inversion method, where each frame has three main panels: the traveltime plotting panel (upper left), used to view and interact with the observed data; the fit and editing panel (upper right), used to edit traveltimes, by clicking on data points and dragging them up or down, and to view the graphical fit between the observed and calculated traveltimes; and the velocity model plotting panel (bottom). 

For calling Refrapick, on your terminal, call:
```bash
refrapy inv
```
For usage, follow the instructions on the video below:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/rOJjxoc2cbU/0.jpg)](https://www.youtube.com/watch?v=rOJjxoc2cbU)

## Reporting errors and asking questions

We encourage users to open an issue in this repository when encountering an error or when in doubt about a functionality or any other subject regarding the use of the software.

## Acknowledgement and citation

If you use Refrapy in your work please cite the following paper:

*Guedes, V.J.C.B., Maciel, S.T.R., Rocha, M.P., 2022. Refrapy: A Python program for seismic refraction data analysis, Computers and Geosciences. https://doi.org/10.1016/j.cageo.2021.105020.*
