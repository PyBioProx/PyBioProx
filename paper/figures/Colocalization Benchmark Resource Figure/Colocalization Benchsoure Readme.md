## Data source

This figure is intended to show the ability of the Perimeter Distance 
measurements to identify changes in ground-truth colocalization. Data is from 
the colocalization benchmark source.

Data is available here: https://www.colocalization-benchmark.com/downloads.html

I have only considered Image Sets 1-3. Image Set 4 has seperated the channels
into seperate images - and who has time for that!

### Image Set 1
Red and Green (channels 1 and 2) objects, Josh's own analysis (comparing
distances of objects in channel 1 to objects in channel 2) shows that 
the PD<sub>mean/median/max</sub> metrics are capable of identifying the 
increasing ground-truth colocalization. PD<sub>min</sub> (edge-edge) 
measurements (i.e. the minimum distance between object in channel 1 to object
in channel 2) are not able to identify differences in ground-truth 
colocalization

Note that images are given as .tiff's. This reads in with different dimensions
to .tif
### Image Set 2

As above, compares channels 1 and 3

### Image Set 3

As above, compares channels 2 and 3

## other notes
It could be an idea to have Manders and Pearson coefficients for each of these
images so we could plot them alongside our measurements to show how our distance
/object based metrics ability to distinguish between ground-truth 
colocalization compares to Manders and Pearson coefficients. 

