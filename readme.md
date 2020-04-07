#PyDist3D: 2 & 3d spatial distance analysis in Python

This module, `pydist3d`, offers efficient 2d and 3d spatial analysis of colocalisation. 
The analyses fall into the category of object-based colocalisation methods. 

## Installation 

To install this Python module, download the module (either as an archive file or 
using a git client) from https://git.exeter.ac.uk/jm544/three-d-distance-analyser. 

Once downloaded (and extracted if using the archive version), install any necessary 
requirements using

```
    pip install -r requirements.txt --user
```

to install the required modules in your user-space modules directory. 
Alternatively if using e.g. a virtualenv or you wish to install the 
dependencies system-wide(!), you can ommit the `--user` flag.

## Getting started

Once installed, the module can be invoked from the command-line using: 

```
    python -m pydist3d <path_to_folder> 
```

to run the analysis in batch mode on all data files at the location `path_to_folder`. 


