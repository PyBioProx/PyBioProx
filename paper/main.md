# Methods

## 1. Macrophage infection assay procedure

J774A.1 cells were routinely cultured in DMEM containing 4500mg/L glucose and 10% FBS and incubated at 37°C with 5% CO 2 . 2.5 x10 5 cells were seeded in 24 well plates containing glass coverslips and grown overnight. Cells were washed 2x with PBS before inoculating with S. aureus MSSA476 carrying the pRN11 (mCherry) expression plasmid (available from) at a MOI of 1. Infection was allowed to proceed for 2hrs, before washing with PBS and treating with 100µg/ml gentamicin in DMEM for 1hr to kill extracellular bacteria. Cells were then washed 3x with PBS and DMEM containing 10µg/ml gentamicin added to prevent bacterial outgrowth. At relevant timepoints, cells were washed with PBS and fixed with 4% paraformaldehyde for 10min at 37°C. Cells were washed with PBS and blocked/permeabilized in a PBS solution containing 0.2% saponin &amp; 5% bovine serum albumin (BSA). Cells were washed in PBS, overlaid with primary antibody (1:100 inblocking/permeabilization solution) and incubated overnight at 4°C. Cells were extensively washed in PBS then overlaid with secondary antibody (1:400 in blocking/permeabilization solution) for 1hr before washing in PBS and mounting on slides containing prolong gold.

## 2. Confocal microscopy

Mounted samples were imaged using the Zeiss LSM 880 laser scanning microscope. **(ask Ana for details). Detail of aperture, magnification, z-stack distance etc.**

## 3. Fluorescent object detection

PyDist3D computes distance between labelled objects in separate fluorescent channels. Prior to detection of fluorescent objects, different pre-processing steps may be performed to enable better object detection. PyDist3D provides a limited number of pre-processing options derived from the `scipy.ndimage` package. In the examples presented in this paper, pre-processing with a multidimensional Gaussian filter (`scipy.ndimage.gaussian_filter`) at a sigma of 1 is used to reduce single-pixel scale noise prior to object detection. Following pre-processing, binary 2D/3D arrays are generated to define regions containing ‘on’ (1) and ‘off’ (0) pixels representing positive and negative signal. PyDist3D provides a range of thresholding methods from the scikit-image package to define positive and negative signal 1 . A comparison operator is then used to generate binary 2D/3D images.Unless specified otherwise, the Otsu thresholding method is used in the examples presented in this paper 2 . Connected regions of ‘on’ pixels are then labelled as unique objects using the `scipy.ndimage.label` function. Size exclusion criteria can then be used to filter the identified objects for a particular size. In this study, objects smaller than 10 (?) connected pixels are considered to be noise and are thus removed. A binary erosion of the labelled objects is then employed to identify its perimeter pixels. Finally, overlays of the detected object’s perimeter on (user-defined)representative z-slices of the original image are generated to allow for confirmation that fluorescent objects have been appropriately labelled.

## 4. Distance analysis

PyDist3D allows for the measurement of distances of the perimeter pixels of objects in one channel to the nearest ‘on’ pixels in another channel. For example, the distances of objects in channel X to objects in channel Y can be measured. Distances analyses are performed using an exact Euclidean distance transform of the fluorescent channel that object distances are measured towards (i.e.channel Y). The distance of each perimeter pixel of the fluorescent object in channel X to the nearest‘on’ pixel in channel Y is then measured. From this data, summary statistics to describe the distance of each object in channel X relative to objects in channel Y are generated. As described subsequently, PyDist3D introduces a statistic termed the ‘distance score’ in which the mean of each perimeter pixel of an object in channel X’s distance to the nearest ‘on’ pixel in channel Y is calculated. Minimum and maximum distances from objects in channel X to the nearest object in channel Y are also generated.

# References

1. van der Walt, S. et al. scikit-image: image processing in Python. PeerJ 2, e453 (2014).
2. Otsu, N. A Threshold Selection Method from Gray-Level Histograms. IEEE Trans. Syst. Man. Cybern. 9, 62–66 (1979).
