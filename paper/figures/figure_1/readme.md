## File contents

*  Two folders have been sent via wetransfer link named “LAMP-1 S. aureus 1.5hr” and “LAMP-1 S. aureus 24hr” 
*  We are comparing the 1.5hr and the 24hr timepoints against eachother 
*  Each file is a .tif derived from the original .czi files that were converted in the zen blue software. Channel 1 shows the bacteria whilst channel 2 shows LAMP-1 - a cellular compartment marker. 

## File naming system

*  Preceding text before each file identifyer: "12-10-18"
*  In this dataset, there are two conditions that we are comparing: a 1hr timepoint and a 24hr timepoint (identifyers in file name = "1hr" & "24hr). 
*  Each condition contains 3 replicate wells (denoted by the number immediately following the timepoint identifyer. 
*  Each well has 5 fields of view described by the identifyer "Scene-x" 
*  For example, the file "12-10-18 1hr 1-Scene-1" is the first field of view of replicate 1 of the 1hr timepoint condition. 

## Analysis
*  The distance from objects in channel 1 to objects in channel 2 will be measured. We identify the mean distance of each of the perimeter pixels of an object in channel 1 to the closest positive signal in channel 2. 
*  The following graphs should be prepared that we will then be able to choose from: 

1. A scatter plot where all mean distances for objects in each condition have been pooled from across the 3 replicate wells. 
2. A scatter plot where the median is taken from each of the three replicate wells for each condition and plotted
3. Figures showing example original images and object detection. 
4. An example image showing a single cell with poor encapsulation in the 24hr condition and good encapsulation in the 1hr condition
Josh will indicate in a future update some useful example images 
