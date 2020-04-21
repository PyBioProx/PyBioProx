# Title

PyDist: Distance-based Image Analysis in Python and Perimeter Distance Measurements to Describe the
Spatial Distributions of Fluorescent Objects.

# Introduction

Determining the co-localization of biomarkers via microscopy is a frequently 
employed method to infer meaningful biological interactions within cells. By
labelling two or more biomarkers with distinct fluorescent tags, the 
biomarkers can be visualized by immunofluorescence microscopy methods. 
Taking single images or multiple images along the Z-axis in the same X/Y axes 
(referred to as a Z-stack), allows the distribution of the biomarkers in 2D or 
3D space to be observed. Once images are captured, the relationship between 
the fluorescently-tagged biomarkers can be assessed. A simplistic analysis 
of colocalization may involve overlaying two fluorescent channels and manually 
assessing regions of fluorescent overlap as colocalization. A range of 
more quantitative co-localization analyses exist ranging in complexity
that can provide more systematic and robust quantification ([1](#1)). 

In this paper, we define a set of simple descriptive measurements
that quantify the spatial relationship of each object in fluorescent 
channel X to objects in fluorescent channel Y. 
Perimeter Distance (PD) measurements are defined in _Fig 1_ 
and detailed extensively in the methods section. In brief, objects in one 
fluorescent channel are detected and the perimeter pixels around the object 
determined. The distance of each pixel in an object's perimeter to the nearest
detected object~~positive fluorescent signal~~ in the second channel is then calculated.

**Josh:^ I CHOSE THE PHRASE 'POSITIVE FLUORESCENT SIGNAL' BECAUSE WE GENERATE OUR
DISTANCE MAP FROM A BINARY MASK OF CHANNEL Y, AS WE HAVEN'T PERFORMED OBJECT
DETECTION ON CHANNEL Y, IS IT ACCURATE FOR US TO SAY THAT WE ARE MEASURING THE DISTANCE
BETWEEN TWO OBJECTS?**

We refer to these pixel-pixel distances as perimeter distance (PD) measurements. 
The units of PD measurements may be pixels/voxels or in real-world units 
(e.g. µm/nm) if pixel/voxel dimensions are known. Depending on the number of 
perimeter pixels, each object may have thousands of PD measurements. We show that
by taking the mean, median or maximum of these PD measurements, we can accuately 
describe the spatial localization of the object relative to objects in another 
fluorescent channel. We refer to these descriptive measurements as 
PD<sub>mean</sub>, PD<sub>median</sub> and PD<sub>max</sub> respectively. 
(_Fig 2, Fig 3_).

We also introduce PyDist, a user-friendly object-based colocalization 
module written in python that generates PD measurements to describe the 
relationships between biomarkers in 2D or 3D space. Analysis of co-localization
by distance measurements is not a novel concept. For example, a tool 
implemented in ImageJ called DiAna allows for the distance-based 
analysis of pairs of differently labelled fluorescent objects [2](#2). The core 
advantages that PyDist introduces include improved speed affording a high aptitude 
for the batch distance-based colocalization analysis of large 2D and 3D 
immunofluorescent datasets, as well as the extensibility of being written in an
easy to learn and very fast to prototype ~in~ programming-language, Python, 
compared with e.g. Java or C++. 



![**Fig 1 PD Measurements Explanation**](paper/figures/PyDist_explanation_figure.png)
***Fig 1 - PD Measurements** An illustrative example is 
shown in which the distance-based colocalization of a
blue fluorescent object relative to red fluorescent objects is assessed. 12
perimeter voxels (illustrated as light-blue boxes) have been identified for the
blue object. The numbers in the centre of each perimeter-voxel refer to PD
measurements: the shortest distance from the perimeter-voxel to the nearest object 
in the red fluorescent signal. The mean and median of all of these PD measurements gives
the PD<sub>mean</sub> and PD<sub>median</sub> measurements respectively. The largest
and smallest of these PD measurements gives the PD<sub>max</sub> and
edge-edge distances respectively.*

# Methods

### 1. Macrophage infection assay procedure

J774A.1 cells were routinely cultured in DMEM containing 4500mg/L glucose and 
10% FBS and incubated at 37°C with 5% CO<sub>2</sub>. 3 replicate wells were 
seeded with 2.5 x 10<sup>5</sup> cells in 24 well plates containing 
glass coverslips and grown overnight. Cells were washed 
2x with PBS before inoculating with S. aureus MSSA476 carrying the pRN11 
(mCherry) expression plasmid at a MOI of 1. Infection was 
allowed to proceed for 2hrs, before washing with PBS and treating with 
100µg/ml gentamicin in DMEM for 1hr to kill extracellular bacteria. Cells were 
then washed 3x with PBS and DMEM containing 10µg/ml gentamicin added to 
prevent bacterial outgrowth. At relevant timepoints, cells were washed with PBS 
and fixed with 4% paraformaldehyde for 10 min at 37°C. Cells were washed with 
PBS and blocked/permeabilized in a PBS solution containing 0.2 % saponin & 
5 % bovine serum albumin (BSA). Cells were washed in PBS, overlaid with primary 
antibody (1:100 inblocking/permeabilization solution) and incubated overnight 
at 4°C. Cells were extensively washed in PBS then overlaid with secondary 
antibody (1:400 in blocking/permeabilization solution) for 1hr before washing 
in PBS and mounting on slides containing prolong gold. Mounted samples were 
imaged using a Zeiss LSM 880 laser scanning microscope using a 100x oil 
immersion objective (NA 1.55). 5 Z-stack images were taken per technical 
replicate with a step size of 0.75µm. Images are available at the Image Data
Resource (IDR number: )


### 2. Fluorescent object detection

PyDist computes distances between labelled objects in separate fluorescence 
channels. Prior to detection of fluorescent objects, different pre-processing 
steps may be performed to improve detection accuracy. PyDist provides a 
small number of pre-processing options derived from the `scipy.ndimage` 
package. Alteratively, due to it's extensible nature, user selected pre-processing functions 
can easily be passed in to the detection function using the straight-forward module
API. 
A second alternative is to pre-process images with another program and pass in 
pre-processed images into PyDist.
Following the optional pre-processing, binary 2D/3D arrays are generated to define regions 
containing foreground or background pixels, using binary values ‘on’ (1) and ‘off’ (0) 
to represent presence or absence of signal respectively. 
PyDist provides a range of thresholding methods from the 
scikit-image package to define what is selected as positive and negative signal [3](#3). 
The Otsu thresholding method is used in the examples presented in this paper [4](#4).
A comparison operator is then used to generate binary 2D/3D images. 
Alternatively, users can provide PyDist with 
binary images that have been previously thresholded in another program. 
Connected regions of ‘on’ pixels are then labelled as unique objects using the 
`scipy.ndimage.label` function. Size exclusion criteria can then also be used to 
filter the identified objects for a particular size range. In the sample data used 
in this paper, objects smaller than 10 connected pixels are considered to be noise and are thus 
removed. A binary erosion of the labelled objects is then employed to identify 
its perimeter pixels. Finally, overlays of the detected object’s perimeter on 
(user-defined) representative z-slices of the original image are generated to 
allow for confirmation that fluorescent objects have been appropriately 
labelled.

### 3. Distance analysis

PyDist allows for the measurement of distances of the perimeter pixels of 
objects in one channel to the nearest _on_ pixels in another channel. For 
example, the distances of objects in channel X to objects in channel Y can be 
measured. Distance analyses are performed using an exact Euclidean distance 
transform of the fluorescent channel that object distances are measured towards 
(i.e.channel Y). The distance of each perimeter pixel of the fluorescent object 
in channel X to the nearest _on_ pixel in channel Y is then measured. From 
this data, summary statistics to describe the distance of each object in 
channel X relative to objects in channel Y are generated. As described 
below, PyDist introduces a statistic termed the _distance score_ 
in which the mean of each perimeter pixel of an object in channel X's 
distance to the nearest _on_ pixel in channel Y is calculated. Minimum and 
maximum distances from objects in channel X to the nearest object in channel Y 
are also generated.

# Results Section

### Example 1 - Advantages of PD measurements over centroid-centroid measurements

In an approach described by several groups and implemented in the DiAna ImageJ
plugin, the distance between pairs of differently labelled fluorescent objects 
is assessed. 
This can be done by measuring the distance between the 
centroids of the objects (centroid-centroid measurements), the edges of the objects
(edge-edge measurements) or the distance between the centre of one object to the
edge of another (centroid-edge measurements) ([2](#2)). In Figure 2, we illustrate
issues with this approach that PD measurements overcome. Within Figure 2A, Image 1
has a larger number of cyan objects that are spatially closely associated with 
the red object then Image 2. Image 1 can thus  be reasonably 
described as having a stronger spatial colocalisation. 
However, if only analysing the closest centroid-centroid pairing, the images
are described as having the same levels of spatial colocalisation (Figure 2B). 
Only when averaging two or more centroid-centroid pairings is Image 1 
identified as having a greater colocalisation than Image 2. This illustrates that
while centroid-centroid measurements can detect differences in spatial colocalisation,
the appropriate number of centroid-centroid measurements to use is not necessarily
obvious and will likely vary from image to image. Measuring both too few or 
too many centroid-centroid measurements may result in poor detection of true differences
in colocalisation, either by excluding colocalised objects from the calculation
or by diluting the colocalisation signal with irrelevant measurements. By contrast,
the PD<sub>mean/median/max</sub> measurements all show clear differences between
Images 1 and 2 with no further analysis decisions needed.

A second issue issue with centroid-centroid measurements that PD measurements 
overcome involves the overreliance of centroid-centroid measurements on 
accurate object detection. Object detection for centroid-centroid measurements
is necessary for both fluorescent channels. PD measurements by contrast, 
require object detection in only one channel. This reduced dependency on 
accurately detecting objects limits the impact of small changes in object 
detection on the average spatial colocalisation of an image. For example, in 
Figure 2A, Image 3 is a duplicate of Image 2 with a small region of null 
signal added to divide the closest cyan object (to the red object) such that
two objects are now detected (as indicated by the white arrowheads). Because
of this small change in the image, when averaging the two, three and four 
closest centroid-centroid measurements, Image 3 is described as being 29.6 %,
29.1 % and 22. 3 % _more_ spatially colocalised then Image 2. By contrast, 
the PD<sub>median</sub> and PD<sub>max</sub> identified no differences between 
Image 2 and Image 3. The PD<sub>mean</sub> measurement correctly identifies 
a very small differnce in spatial colocalisation of Image 2 and 3 (95.810 and 
95.812 pixels respectively), reflecting the small region of null signal added
in Image 3. The PD<sub>min</sub> (edge-edge) measurement is unable to 
differentiate between all three images and thus is inappropriate in this
instance. 


![**Fig 2 PD measurements provide more robust descriptions of spatial distances then centroid-centroid measurements**](paper/figures/Centroid-Centroid-Figure.png)
**Fig 2 PD measurements provide more robust descriptions of spatial distances then centroid-centroid measurements**
**(A)**Images generated using Inkscape software with random
pixel noise added in Python to better resemble true microscopy images. The
red signal in each image is in the same spatial location each time. As discussed
in the text, the distribution of the blue signal is altered. Images 2 and 3 are
identical but for a region of null signal added in image 3 to divide the object
indicated by white arrow heads into two objects. **(B)** Distance measurements of
each image. Centroid-centroid distances were calculated in DiAna using default
parameters ([2](#2)). The ‘Closest’ centroid-centroid measurement describes the
centroid-centroid distance between the red object and the nearest blue object.
The “Two Closest” – “Four Closest” centroid-centroid measurements describe
the average (mean) between the red object and the two – four closest blue
objects. PD measurements were calculated using PyDist as previously
described.

### Example 1 - Capacity of different PD measurements to determine colocalization

The Colocalization Benchmark Source (CBS) is 
an online database of 2D computer-simulated images with pre-defined 
(ground truth) values of pixel-based co-localization ranging from 0-90
To validate the capacity of this approach to detect changes in even pixel-level 
colocalization, we utilized Image Set 1 from the CBS. Images 
were processed using PyDist as described in the methods section. Example CBS images
with ground-truth colocalization values of 10%, 50% and 90% are shown 
(_Fig 2A_). The PD<sub>mean</sub> for each fluorescent
object in channel 1 relative to the fluorescence in channel 2 in the 10%, 50% 
and 90% images were calculated (_Fig 2B_). 1544, 1592 and 1588 objects in channel 1 were 
detected for the 10%, 50% and 90% images respectively. 
Significantly different distributions of PD<sub>mean</sub> values for each image
are observed. The PD<sub>mean</sub> values for the magenta objects in the 10% colocalization image
have a wide distribution, with PD<sub>mean</sub> values that cluster between
5 and 10 pixels  Contrastingly, PD<sub>mean</sub> values for the magenta objects 
of the 50% and 90% (ground-truth) colocalization condition cluster progressively
nearer to 0 pixels reflecting the higher degree of colocalization (_Fig 2B_). 

The mean PD<sub>mean</sub>, PD<sub>median</sub>, 
PD<sub>max</sub> and edge-edge distance measurements of the 
objects in the red channel of CBS dataset 1 are plotted (_Figs 2C-F_)
to visualize how
they may result in different interpretations. As expected, the mean
PD<sub>mean/median/max</sub> values for each image decreases as ground truth
% colocalization increases. In
_Supp. Fig 1 & 2_, CBS data sets 2 and 3 are analysed. Similarly, the mean 
PD<sub>mean/median/max</sub> values consistantly decrease as ground truth %
colocalization increases. This demonstrates that PD<sub>mean/median/max</sub>
measurements are sufficient to identify ground-truth colocalization differences in 
a 2D computer-generated image dataset.  By contrast, edge-edge values 
do not decrease on average with increasing ground-truth % colocalization (_Fig 2F_)
demonstrating that edge-edge distance measurements cannot reliably identify 
changes in ground-truth colocalization. Similar
results are seen by analysis of CBS datasets 2 & 3 (_Supp Fig 1D, Supp Fig 2D_).
The poor performance of the edge-edge measurements reflects 
the fact that only the closest pixel in a magenta object to green fluorescent
signal is used in edge-edge measurements. As such, a poorly colocalizing object with a 
PD<sub>mean</sub> distance of 10 pixels could conceivably have an edge-edge 
distance of 0 pixels. As the CBS datasets represent crowded images, 
with large numbers of objects in close proximity to one-another, 
edge-edge distances are inappropriate and likely to give eroneous results. 


![**Fig 2 Colocalization Benchmark Source**](paper/figures/Fig_2_coloc_benchmark_131019.png)
***Fig 2 - PD measurments identify known changes in colocalization** 
**(A)** Representative images of the CBS Data Set 1 with known ground-truth
colocalization values. The red channel in the CBS Data Set 1 is displayed in 
magenta for better visualization. 
**(B)** PD<sub>mean</sub> values for each of the magenta objects in **(A)**. 
P-values were assessed using students t-test \*\*\*\*  = P<0.001. **(C-F)** The average 
PD<sub>mean/median/max</sub> & edge-edge measurements $`\pm`$ 95% CI for objects
the magenta channel of the CBS dataset 1.*

### Example 2 - Fluorescent 3D confocal microscopy & PyDist reveals escape of S. aureus from LAMP-1 positive vesicles at a 24h timepoint

The internalization of bacteria by innate immune cells such as macrophages is 
an important mechanism to contain microbial threats. 
Phagocytosis is a complex process involving the internalization of foreign 
particles such as bacteria and apoptotic cells into a benign compartment 
termed the nascent phagosome. A complex series of maturation events then 
occur in which the nascent phagosome rapidly changes its membrane composition
and inter-luminal contents to form a microbicidal compartment termed the 
phagolysosome.  Whether or not bacteria reside within the mature phagolysosome 
during infection provides important information about the bacteria’s mechanisms
of immune evasion(**Refs needed**). Lysosome-Associated-Membrane-Protein 1 (LAMP1) is a regularly utilized marker 
of the phagolysosome [5](#5)-[9](#9).  Significant overlap in fluorescent signal is not expected between 
bacteria and LAMP-1. Instead, a ‘halo’ of LAMP-1 around a bacterium (_Fig 3A_)
indicates the localization of the bacteria within a phagolysosome[5](#5)-[9](#9). 
Typically, analyses of the extent of LAMP-1 encapsulation around bacteria are 
user-defined binary measures; manually counting the number of positive/negatively 
LAMP-1-associated bacteria in a dataset of blinded images [5](#5)-[9](#9). 
This method of analysis is time-consuming and raises issues of reproducibility.
Defining what amount of LAMP-1 association equates to a positively LAMP-1 
associated bacteria is subjective and may vary from researcher to researcher. 
The binary nature of the analysis may also result in the loss of important 
information as small but meaningful changes in the extent of bacterial 
encapsulation by LAMP-1 may not be identifiable by eye. 

The capacity of Staphylococcus aureus to survive for extended periods of time
within macrophages has become increasingly apparent 
[4](#4)–[6](#6),[7](#7),[8](#8). Recent work indicates a capacity of S. aureus 
to survive and even replicate within LAMP-1 positive vesicles [1](#1)–[2](#2). 
Escape of _S. aureus_ strains from the phagolysosomes of THP-1 cells
and primary human macrophages has also been reported (references 1/2 respectively). We prepared
an infection model of the S. aureus MSSA476 strain in the J774A.1 murine 
macrophage cell line. At early (1.5hr) and late (24hr) timepoints, LAMP-1 
encapsulation of mCherry tagged S. aureus MSSA476 was captured by 
immunofluorescence Z-stack confocal microscopy. Example images of positively
and weakly LAMP-1-associated bacteria are shown (_Fig 3A_).

Prior to processing these images in PyDist, the LAMP-1 channel was pre-processed
by unsharp masking the images in imageJ. Unsharp masking produces a sharpened image 
by subtracting a blurred copy of the image from the orignial 
and rescaling the histogram to produce the original contrast in low
frequncy features. Unsharp masking resulted in a more 
descrete detection of positive LAMP-1 signal (_Supp. Fig 3A_) and a greater capacity
to resolve differences in co-localization as evidenced by larger
PD<sub>mean/median/max</sub> values (_Supp. Fig 3B_). Further pre-processing was performed using a 
multidimensional Gaussian filter (`scipy.ndimage.gaussian_filter`) at a sigma 
of `1` in PyDist to reduce single-pixel scale noise prior to object detection.

Following pre-processing, the PD<sub>mean</sub> for each bacterial cluster in 3D space 
at early and late timepoints 
was calculated in PyDist relative to LAMP-1 fluorescence. _Fig 3B_ shows a 
swarm plot of these measurements. Notably, a larger number of 
bacterial clusters were detected by PyDist at the 24 hr timepoint then 
at the 1.5hr timepoint. A 2.44 fold increase in the mean PD<sub>mean</sub> 
is seen for the 24hr timepoint compaired to the 1.5 hr timepoint. 
These PD<sub>mean</sub> values are displayed in _Fig 3C_ 
as a frequency distribution. Clear differences in the percentage distribution of 
bacterial PD<sub>mean's</sub> can be observed at the early and late timepoints. 
The percentage distribution of PD<sub>mean</sub> values at 1.5 hrs has a 
positive skew with a peak between 0-0.0325µm. By contrast, at the 24 hr 
timepoint, PD<sub>mean</sub> values appear to have a normal distribution, 
with a peak between 0.125-0.250µm. Thus, in this infection model, 
PyDist analysis suggests that _S. aureus_ MSSA476 is less likely to be found
encapsulated by LAMP-1 at late compared to early timepoints. This is
consistent with previous findings that _S. aureus_ is capable of escape from
LAMP-1 positive vesicles [5](#5),[10](#10).

![**Fig 3 PyDist3D identifys the escape of S. aureus from LAMP-1 positive vesicles**](paper/figures/LAMP-1_Fig_121119.png)
**Fig 3 PyDist3D identifys the escape of _S. aureus_ from LAMP-1 positive vesicles**
**(A)** Representative examples of _S. aureus_ with strong and weak LAMP-1 
associations. A single slice of a Z-stack is shown. An unsharp mask pre-filtering
operation has been applied to the LAMP-1 channel of these images to enable better object detection.
**(B)** All PD<sub>mean</sub> values for each detected _S. aureus_ object relative
to LAMP-1 positive signal across early (1.5 hr) and late (24 hr) timepoints
**(C)** The _S. aureus_ PD<sub>mean</sub> values for early and late timepoints 
from **(B)** displayed as a frequency distribution.


## Conclusion

In this paper we introduced PyDist: a user friendly open-source image-analysis tool 
that quantifies the relative spatial localization of fluorescent objectsin 2D 
and 3D immunofluorescent microscopy datasets.
Despite technically being an _object_-based colocalisation framework, we have shown 
that PyDist is able to be used on simulated data meant for assessing pixel-based 
colocalisation measures. 
We have also suggested a set of measurements to describe the relative 
spatial colocalization of these fluorescent objects (PD<sub>mean</sub>,
PD<sub>median</sub> & PD<sub>max</sub>). These measures appear to have a strong
capacity to accurately describe ground-truth colocalization values in a 
2D dataset(_Fig 2_). The applicability of PyDist analysis to make biological relevant observations 
was then assessed. Using the PD<sub>mean</sub> measurement, we were able to 
identify significant differences in the colocalization of _S. aureus_ with a 
marker of an intracellular compartment at early and late timepoints (_Fig 3_). 
Collectively these results suggest that PyDist analysis and the perimeter 
distance (PD) measurements described in this paper can function as a powerful 
means of analysing the relative spatial colocalization of fluorescent biomarkers. 

## Results References
<a name="1">1.</a> Bolte, S. & Cordelières, F. P. A guided tour into subcellular 
colocalization analysis in light microscopy. J. Microsc. 224, 213–232 (2006).

<a name="2">2.</a> Gilles, J.-F., Dos Santos, M., Boudier, T., Bolte, S. & 
Heck, N. DiAna, an ImageJ tool for object-based 3D co-localization 
and distance analysis. Methods 115, 55–64 (2017).

<a name="3">3.</a> van der Walt, S. et al. scikit-image: image processing in 
Python. PeerJ 2, e453 (2014).

<a name="4">2.</a> Otsu, N. A Threshold Selection Method from Gray-Level 
Histograms. IEEE Trans. Syst. Man. Cybern. 9, 62–66 (1979).

<a name="5">5.</a> Flannagan, R. S., Heit, B. & Heinrichs, D. E. Intracellular
replication of Staphylococcus aureus in mature phagolysosomes in macrophages 
precedes host cell death, and bacterial escape and dissemination. 
Cell. Microbiol. 18, 514–535 (2016).

<a name="6">6.</a> Jubrail, J. et al. Inability to sustain intraphagolysosomal
killing of Staphylococcus aureus predisposes to bacterial persistence in 
macrophages. Cell. Microbiol. 18, 80–96 (2016).

<a name="7">7.</a> Surewaard, B. G. J. et al. Identification and treatment of 
the Staphylococcus aureus reservoir in vivo. J. Exp. Med. 213, 1141–51 (2016).

<a name="8">8.</a>.	Custódio, R. et al. Characterization of secreted 
sphingosine-1-phosphate lyases required for virulence and intracellular
survival of Burkholderia pseudomallei. Mol. Microbiol. 102, 1004–1019 (2016).

<a name="9">9.</a> Dallenga, T. et al. M. tuberculosis-Induced Necrosis of 
Infected Neutrophils Promotes Bacterial Growth Following Phagocytosis by 
Macrophages. Cell Host Microbe 22, 519-530.e3 (2017).

<a name="10">10.</a> Grosz, M. et al. Cytoplasmic replication of Staphylococcus
aureus upon phagosomal escape triggered by phenol-soluble modulin α. 
doi:10.1111/cmi.12233

<a name="11">11.</a> Kubica, M. et al. A Potential New Pathway for Staphylococcus 
aureus Dissemination: The Silent Survival of S. aureus Phagocytosed by Human 
Monocyte-Derived Macrophages. PLoS One 3, e1409 (2008).


## Supplemental Figures. 

![**Supp. Fig 1 - PyDist analysis of CBS dataset 2**](paper/figures/Supp_Fig_CBS_Data_Set_2.png)
**Supp. Fig 1 - PyDist analysis of CBS dataset 2**
**(A-D)** The average 
PD<sub>mean/median/max</sub> & edge-edge measurements $`\pm`$ 95% CI for objects
the red channel of CBS dataset 2.*

![**Supp. Fig 2 - PyDist analysis of CBS dataset 3**](paper/figures/Supp_Fig_CBS_Data_Set_3.png)
**Supp. Fig 2 - PyDist analysis of CBS dataset 3**
**(A-D)** The average 
PD<sub>mean/median/max</sub> & edge-edge measurements $`\pm`$ 95% CI for objects
the green channel of the CBS dataset 3.*

![**Supp. Fig 3 - Impact of Unsharp Mask Pre-processing**](paper/figures/Supp_Fig_Unsharp_Mask.png)
**Supp. Fig 3 - Impact of Unsharp Mask Pre-processing**
**(A)** The objects identified by PyDist following an unsharp mask processing operation 
on the LAMP-1 channel only. **(B)** The PD<sub>Mean/Median/Max</sub> and edge-edge measurements
of the image shown in **(A)** with and without unsharp mask pre-processing
