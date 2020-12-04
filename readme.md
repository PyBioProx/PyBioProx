# PyBioProx: 2 & 3d spatial distance analysis in Python

This module, `pybioprox`, offers efficient 2d and 3d spatial analysis of colocalisation. 
The analyses fall into the category of object-based colocalisation methods. 

## Installation 

To install this Python module, you may use pip as follows: 

```
    pip install pybioprox 
```

If you wish to also install the optional Graphical User Interface script, this may be done 
by specifying the `gui` optional extra: 

```
    pip install pybioprox[gui]
```


## Getting started

Once installed, the module can be invoked from the command-line using: 

```
    python -m pybioprox <path_to_folder> 
```

to run the analysis in batch mode on all data files at the location `path_to_folder`. 

If you have installed the gui component or already have the required gui libraries, 
present on your system, then you may also run 
```
    pybioprox_gui
```
directly from the command line. 
