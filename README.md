![alt text](https://github.com/viictorjs/Refrapy/blob/master/refrapy_logo.png)

## Introduction

Refrapy is a Python software package with a graphical interface for seismic refraction data analysis. 

It is based on two modules: Refrapick and Refrainv.

The Refrapick program is used for basic waveform processing for first breaks picking. The waveform reading is powered by ObsPy (https://www.obspy.org/).

The Refrainv program is used to run a time-terms and a traveltimes tomography inversion. The latter is powered by pyGIMLi (https://www.pygimli.org/).

All dependencies are listed below:
   ```
   numpy
   matplotlib
   scipy
   obspy
   pygimli
   tkinter
   ```

It is recommended the use of Anaconda (https://www.anaconda.com/), because it simplifies package management.
Once it is installed, open run the following commands on Anaconda prompt:

   ```
   conda create -n refrapy python=3.7.7
   conda activate refrapy
   conda install obspy
   conda install -c gimli -c conda-forge pygimli=1.0.12
   ```
    
Once all the necessary packages are installed, extract Refrapick.py, Refrainv.py and the images folder to a directory on your computer. 

You can execute the python files by running:

   ```
   python Refrapick.py
   python Refrainv.py
   ```
   
## Contributors

Victor Guedes (vjs279@hotmail.com)
Susanne Maciel (susanne@unb.br)
Marcelo Rocha (marcelorocha@unb.br)

## Refrapick

**Open waveform files**: the software is aimed to work mainly around SEG2 files, but all waveform formats readable by ObsPy can be used. However, there are a few conditions that need to be considered when reading multichannel waveform data. Waveform **files with missing data traces cannot be used as input**, which can occur with files that have already passed through some other processing software, where one or more traces were removed manually, probably due to being bad noisy data. Thus, **it is recommended the use of original files (i.e., without any editing)**. Also, receivers and source position may not be well defined in the file header or may fail to be properly read. **In such cases, instead of obtaining this information automatically (conventional attempt), dialog boxes appear so that the user can enter these required values**.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/open_waveform.gif)

**Basic waveform processing**: Normalization divides amplitudes by each trace’s maximum amplitude. Scale gain divides (decrease gain) or multiplies (increase gain) the amplitudes of the current section by a fixed factor. High pass/Low pass filters removes unwanted frequency content of the current section, where each consecutive application will assign a new frequency limit following a fixed factor. Traces can be plotted with the filling of the positive/negative side of amplitudes or as simple wiggles (no filling). All amplitudes superposition can be clipped. A trimming mode can be enabled/disabled: clicking on the plotting screen will assign the y value of the clicked position as a limit, where all samples in the current section after that time will be removed. This function is particularly useful when there are data sets with high sampling frequency, where **removing samples might speed up the performance of other functions**.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/norm_gain_fill.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/filters.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/trim_samples.gif)

**Get apparent velocity**: An interaction mode can be enabled/disabled to obtain the apparent velocity of a layer (Va), that can be estimated by drawing a straight line on the current section. The inverse of the calculated slope of the line is plotted as Va.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/apparent_velocity.gif)

**Picking first breaks**: An interaction mode can be enabled/disabled for first breaks picking. Picks can be made individually with single clicks or several at once. The latter can be done by drawing a straight line through the section, where intersections with traces will be marked as picks. Only one pick can be created per trace, so that a pick already made will be changed to a new y value if a new click occurs. A line connecting all the picks of the current section can be plotted. All picks of the current section can be removed. A preview of the resulting traveltime curves can be checked any time, with an interaction mode to  manually highlight erroneous picks and facilitate its identification between sections. Figure functions (e.g. zoom, pan) are available in the Matplotlib's toolbar. All picks can be exported into a single file, usable for data inversion latter.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick3.gif)

If a new data set is to be analyzed or if it is necessary to open more sections in addition to those already read, **it is necessary to reset all memory and plotting screens**.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/reset.gif)

## Refrainv

The inversion methods of time-terms analysis and traveltime tomography are available in the Refrainv program . The program presents an individual frame for each inversion method, where each frame has three main panels: the traveltime plotting panel (upper left), used to view and interact with the observed data; the fit and editing panel (upper right), used to edit traveltimes, by clicking on data points and dragging them up or down, and to view the graphical fit between the observed and calculated traveltimes; and the velocity model plotting panel (bottom). 

**Time-terms inversion**: The pick file exported from Refrapick can used directly used as input for a time-terms analysis in Refrainv. To show the y axis of a velocity model as elevation instead of depth, a two-column topography file can be entered right before running the time-terms inversion. A custom regularization weight can be entered (higher the value, smoother the model). The goodness-of-fit can be evaluated graphically and through RMS errors. The time-terms model can be exported as a column file with the geometry and velocity values of the layers. Some plot customizations can be made.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv1.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv3.gif)

**Traveltimes tomography inversion**: It is previously necessary to use the implemented conversion function to create a file readable by pyGIMLi’s traveltime manager from the pick file exported in Refrapick. To show the y axis of a velocity model as elevation instead of depth, a two-column topography file can be entered when creating the traveltimes tomography file. The following mesh and inversion parameters can be entered: maximum mesh depth, maximum mesh cell size, relative distance for refinement nodes of a mesh cell, number of secondary nodes in mesh cells, minimum and maximum velocities of a gradient starting model, relative weight in vertical to horizontal direction, total penalty factor for the model roughness and maximum number of iterations. The goodness-of-fit can be evaluated graphically and through RMS errors and Chi² value. The velocity tomogram can be exported as a xyz file, containing the velocity and centers positions of all cells. Some plot customizations can be made.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/tomography_inv1.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/tomography_inv2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/tomography_inv3.gif)

