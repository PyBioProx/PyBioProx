# Title

A distance-based image analysis tool and novel distance metrics to describe the
spatial distributions of fluorescent objects in microscopy images

# Introduction

Detecting the co-localization of biomarkers via microscopy is a frequently 
employed method to infer meaningful biological interactions within cells. By
labelling two or more biomarkers with distinct fluorescent tags, the 
biomarkers can be visualized by immunofluorescence microscopy methods.  
Taking single or multiple images along the z-axis in the same X/Y axes 
(referred to as a z-stack), the distribution of the biomarkers in 2D or 
3D space can be observed. Once images are captured, the relationship between 
the fluorescently-tagged biomarkers can then be assessed. A simplistic analysis 
of colocalization may involve overlaying two fluorescent channels and manually 
identifying regions of fluorescent tag overlap as colocalization. A range of 
more sophisticated automated co-localization analyses exist, and can be broadly 
grouped into pixel-based and object-based methods (**refs**).

In this paper, we introduce PyDist; a user-friendly object-based colocalization 
set of modules written in python that uses distance measurements to describe the 
relationships between biomarkers in 2D or 3D space. Analysis of co-localization
by distance measurements is not a novel concept. For example, an excellent tool 
implemented in ImageJ called DiAna allows for the detailed distance-based 
analysis of pairs of differently labelled fluorescent objects (**ref**). The core 
advantages that PyDist brings include improved speed affording a high aptitude 
for the batch distance-based colocalization analysis of large 2D and 3D 
immunofluorescent datasets, as well as the extensibility of being written in a 
much easier to learn language like Python, compared with e.g. Java or C++. 

~~PyDist produces a novel set of simple and intuitive distance-based metrics of 
colocalization that describe the relationship of each fluorescent object in one 
channel to the fluorescent signal in another channel. These metrics are termed 
Perimeter Distance Mean (PD<sub>mean</sub>), Perimeter Distance Median 
(PD<sub>median</sub>), and Perimeter Distance Maximum (PD<sub>max</sub>). 
To our knowledge, these metrics have not previously been defined.~~

** crossed-out section replaced with the below**
This paper defines a set of descriptive measurements that quantify the spatial
relationship of each object in fluorescent channel X to objects in fluorescent
channel Y. Perimeter Distance (PD) measurements are defined in **PyDist_explanation fig** 
are detailed extensively in the methods section. In brief, objects in one 
fluorescent channel are detected and the perimeter pixels around the object 
determined. The distance of each pixel in an object's perimeter to the nearest
positive fluorescent signal in the second channel is then calculated. 
The units of this distance may be pixels/voxels or in real-world units 
(e.g. µm/nm) if pixel/voxel dimensions are known. The relative distance of this 
object in channel 1 to objects in channel 2 can now be described by taking the
mean, median, maximum or minimum of these PD measurements 
(to give PD<sub>mean/median/max</sub> or "edge-edge" measurements respectively.
We show that these metrics can function as alternatives to traditional metrics 
of co-localization such as Manders/Persons coefficients, and can provide 
powerful insights into the relative spatial distributions of fluorescent biomarkers.

# Methods

### 1. Macrophage infection assay procedure

J774A.1 cells were routinely cultured in DMEM containing 4500mg/L glucose and 
10% FBS and incubated at 37°C with 5% CO 2 . 2.5 x10 5 cells were seeded in 24 
well plates containing glass coverslips and grown overnight. Cells were washed 
2x with PBS before inoculating with S. aureus MSSA476 carrying the pRN11 
(mCherry) expression plasmid (available from) at a MOI of 1. Infection was 
allowed to proceed for 2hrs, before washing with PBS and treating with 
100µg/ml gentamicin in DMEM for 1hr to kill extracellular bacteria. Cells were 
then washed 3x with PBS and DMEM containing 10µg/ml gentamicin added to 
prevent bacterial outgrowth. At relevant timepoints, cells were washed with PBS 
and fixed with 4% paraformaldehyde for 10min at 37°C. Cells were washed with 
PBS and blocked/permeabilized in a PBS solution containing 0.2% saponin & 
5% bovine serum albumin (BSA). Cells were washed in PBS, overlaid with primary 
antibody (1:100 inblocking/permeabilization solution) and incubated overnight 
at 4°C. Cells were extensively washed in PBS then overlaid with secondary 
antibody (1:400 in blocking/permeabilization solution) for 1hr before washing 
in PBS and mounting on slides containing prolong gold.

### 2. Confocal microscopy

Mounted samples were imaged using the Zeiss LSM 880 laser scanning microscope. 
**(ask Ana for details). Detail of aperture, magnification, z-stack distance 
etc.**

### 3. Fluorescent object detection

PyDist computes distances between labelled objects in separate fluorescence 
channels. Prior to detection of fluorescent objects, different pre-processing 
steps may be performed to improve detection accuracy. PyDist provides a 
limited number of pre-processing options derived from the `scipy.ndimage` 
package. In the examples presented in this paper, pre-processing with a 
multidimensional Gaussian filter (`scipy.ndimage.gaussian_filter`) at a sigma 
of `1` is used to reduce single-pixel scale noise prior to object detection. 
Following pre-processing, binary 2D/3D arrays are generated to define regions 
containing ‘on’ (1) and ‘off’ (0) pixels representing positive and 
negative signal. PyDist provides a range of thresholding methods from the 
scikit-image package to define positive and negative signal [1](#1). 
A comparison operator is then used to generate binary 2D/3D images. Unless 
specified otherwise, the Otsu thresholding method is used in the examples 
presented in this paper [2](#2). Alternatively, users can provide PyDist with 
binary images that have been previously thresholded in another program. 
Connected regions of ‘on’ pixels are then labelled as unique objects using the 
`scipy.ndimage.label` function. Size exclusion criteria can then be used to 
filter the identified objects for a particular size. In this study, objects 
smaller than 10 connected pixels are considered to be noise and are thus 
removed. A binary erosion of the labelled objects is then employed to identify 
its perimeter pixels. Finally, overlays of the detected object’s perimeter on 
(user-defined)representative z-slices of the original image are generated to 
allow for confirmation that fluorescent objects have been appropriately 
labelled.

### 4. Distance analysis

PyDist allows for the measurement of distances of the perimeter pixels of 
objects in one channel to the nearest _on_ pixels in another channel. For 
example, the distances of objects in channel X to objects in channel Y can be 
measured. Distances analyses are performed using an exact Euclidean distance 
transform of the fluorescent channel that object distances are measured towards 
(i.e.channel Y). The distance of each perimeter pixel of the fluorescent object 
in channel X to the nearest _on_ pixel in channel Y is then measured. From 
this data, summary statistics to describe the distance of each object in 
channel X relative to objects in channel Y are generated. As described 
subsequently, PyDist3D introduces a statistic termed the _distance score_ 
in which the mean of each perimeter pixel of an object in channel X's 
distance to the nearest _on_ pixel in channel Y is calculated. Minimum and 
maximum distances from objects in channel X to the nearest object in channel Y 
are also generated.

![example figure markdown thing](./figures/figure1/blah.png) 


### Methods References

<a name="1">1.</a> van der Walt, S. et al. scikit-image: image processing in 
Python. PeerJ 2, e453 (2014).

<a name="2">2.</a> Otsu, N. A Threshold Selection Method from Gray-Level 
Histograms. IEEE Trans. Syst. Man. Cybern. 9, 62–66 (1979).

# Results Section

### Example 1 - Capacity of different PD measurements to determine colocalization

To validate the capacity of this approach to detect changes in colocalization, 
we utilized Image Set 1 from the Colocalization Benchmark Source (CBS). Images 
were processed using PyDist as described in the methods section.CBS is 
an online database of 2D computer-simulated images with pre-defined 
(ground truth) values of co-localization ranging from 0-90%. The PD values for 
objects in the red channel to objects in the green channel were determined as 
previously described. In fig x , the PD<sub>mean</sub> for each red fluorescent
object in the 10% and 90% colocalization images is plotted (1582 and 1592 
objects were detected for the 10% and 90% images respectively).  As expected, 
the PD<sub>mean</sub> values for the red objects of the 90% (ground-truth) 
colocalization condition cluster near 0 pixels reflecting the high degree of 
colocalization. In contrast, the PD<sub>mean</sub> values for the red objects
in the 10% (ground-truth) colocalization condition have a wide distribution. 
Significant distances as analysed by students t-tests are observed.

In **figs 2** , the mean and median PD<sub>mean</sub>, PD<sub>median</sub>, 
PD<sub>max</sub> and PD<sub>min</sub> (edge-edge) distance metrics are plotted
against the ground truth colocalization values for each image to visualize how
they may result in different interpretations of PD data. As expected, the mean
PD<sub>mean/median/max</sub> value for each image decreases as the ground truth
% colocalization increases. Whilst the median PD<sub>mean/median/max</sub> 
values also decrease with increasing ground truth colocalization, for both the
80% and 90% co-localization images, the median PD<sub>mean/median/max</sub> 
value is 0 pixels, thus not allowing for differentiation of these images. In
**supp figs**, CBS data sets 2 and 3 are analysed. Similarly, the mean 
PD<sub>mean/median/max</sub> values consistantly decrease as ground truth %
colocalization increases. Median PD<sub>mean/median/max</sub> values are less 
consistent in their ability to identify small differences in ground-truth % 
colocalization (e.g. 50%-60% in **supp fig**).

By contrast, neither median or mean PD<sub>min</sub> (edge-edge) distances can
reliably identify increasing colocalization. The median PD<sub>min</sub> 
(edge-edge) distance for all ground-truth colocalization conditions is 0 pixels
and thus is not capable of identifying differences in colocalization. The mean 
PDmin (edge-edge) values do not appear to reliably decrease with increasing 
ground-truth % colocalization. 

### Example 2 - Fluorescent 3D confocal microscopy & PyDist reveals escape of S. aureus from LAMP-1 positive vesicles at a 24h timepoint

The internalization of bacteria by innate immune cells such as macrophages is 
an important mechanism to contain microbial threats (**Refs needed**). 
Phagocytosis is a complex process involving the internalization of foreign 
particles such as bacteria and apoptotic cells into a benign compartment 
termed the nascent phagosome. A complex series of maturation events then 
occur in which the nascent phagosome rapidly changes its membrane composition
and inter-luminal contents to form a microbicidal compartment termed the 
phagolysosome.  Whether or not bacteria reside within the mature phagolysosome 
during infection provides important information about the bacteria’s mechanisms
of immune evasion. 

Lysosome-Associated-Membrane-Protein 1 (LAMP1) is a regularly utilized marker 
of the phagolysosome. A ‘halo’ of LAMP-1 around a bacterium as shown in fig(x) 
indicates the localization of the bacteria within a phagolysosome. Typically, 
analyses of the extent of LAMP-1 encapsulation around bacteria are user-defined
binary measures; manually counting the number of positive/negatively 
LAMP-1-associated bacteria in a dataset of blinded images [3](#3)-[7](#7). 
This method of analysis raises issues of reproducibility due to the somewhat
subjective nature of defining what amount of LAMP-1 association equates to a 
positively LAMP-1 associated bacteria. The binary nature of the analysis may 
also result in the loss of important information as small but significant 
changes in the extent of bacterial encapsulation by LAMP-1 may not be 
identifiable by eye. PyDist provides an unbiased, quantitative means of 
assessing the association of bacteria to cellular compartment markers. 

The capacity of Staphylococcus aureus to survive for extended periods of time
within macrophages has become increasingly apparent 
[3](#3)–[5](#5),[6](#6),[7](#7). Recent work indicates a capacity of S. aureus 
to survive and even replicate within LAMP-1 positive vesicles 1,2. Escape of 
S. aureus strains from the phagolysosomes of THP-1 cells and primary human
macrophages has also been reported (references   1/2 respectively). We prepared
an infection model of the S. aureus MSSA476 strain in the J774A.1 murine 
macrophage cell line. At early (1.5hr) and late (24hr) timepoints, LAMP-1 
encapsulation of mCherry tagged S. aureus MSSA476 was captured by 
immunofluorescence z-stack confocal microscopy and analysed by PyDist3D.
As shown in (fig), the PD<sub>mean</sub> for individual S. aureus are 
significantly smaller at 1.5hrs then at 24hrs. Thus, in this infection model, 
PyDist3D analysis suggests that S. aureus MSSA476 is significantly less likely
to be encapsulated by LAMP-1 at late compared to early timepoints. This appears 
to be consistent with previous findings that S. aureus is capable of escape 
from the phagolysosome [3](#3),[8](#8).

## Results References

<a name="3">3.</a> Flannagan, R. S., Heit, B. & Heinrichs, D. E. Intracellular
replication of Staphylococcus aureus in mature phagolysosomes in macrophages 
precedes host cell death, and bacterial escape and dissemination. 
Cell. Microbiol. 18, 514–535 (2016).

<a name="4">4.</a> Jubrail, J. et al. Inability to sustain intraphagolysosomal
killing of Staphylococcus aureus predisposes to bacterial persistence in 
macrophages. Cell. Microbiol. 18, 80–96 (2016).

<a name="5">5.</a> Surewaard, B. G. J. et al. Identification and treatment of 
the Staphylococcus aureus reservoir in vivo. J. Exp. Med. 213, 1141–51 (2016).

<a name="6">6.</a>.	Custódio, R. et al. Characterization of secreted 
sphingosine-1-phosphate lyases required for virulence and intracellular
survival of Burkholderia pseudomallei. Mol. Microbiol. 102, 1004–1019 (2016).

<a name="7">7.</a> Dallenga, T. et al. M. tuberculosis-Induced Necrosis of 
Infected Neutrophils Promotes Bacterial Growth Following Phagocytosis by 
Macrophages. Cell Host Microbe 22, 519-530.e3 (2017).

<a name="8">8.</a> Grosz, M. et al. Cytoplasmic replication of Staphylococcus
aureus upon phagosomal escape triggered by phenol-soluble modulin α. 
doi:10.1111/cmi.12233

<a name="9">9.</a> Kubica, M. et al. A Potential New Pathway for Staphylococcus 
aureus Dissemination: The Silent Survival of S. aureus Phagocytosed by Human 
Monocyte-Derived Macrophages. PLoS One 3, e1409 (2008).

## Conclusion

In this paper we introduced PyDist: a user friendly open-source image-analysis tool 
that quantifies the relative spatial localization of fluorescent objectsin 2D 
and 3D immunofluorescent microscopy datasets. 
We have also suggested a set of new metrics to describe the relative 
spatial colocalization of these fluorescent objects (PD<sub>mean</sub>,
PD<sub>median</sub> & PD<sub>max</sub>). These metrics appear to have a strong
capacity to accurately describe ground-truth colocalization values (**fig**). 
PD<sub>mean</sub> in particular was highly consistent in its ability to identify 
known increases in % colocalization. 

The applicability of PyDist analysis to make biological relevant observations 
was then assessed. Using the PD<sub>mean</sub> metric, we were able to 
identify significant differences in the colocalization of _S. aureus_ with a 
marker of an intracellular compartment at early and late timepoints. These 
observations were confirmed by blinded manual analyses. Traditional pixel-
based measures of colocalization such as Manders and Pearsons coefficients were 
not capable of identifying these differences. Collectively these 
results suggest that PyDist analysis and the perimeter distance (PD) metrics 
described in this paper can function as a powerful means of analysing the
relative spatial colocalization of fluorescent biomakers. 

