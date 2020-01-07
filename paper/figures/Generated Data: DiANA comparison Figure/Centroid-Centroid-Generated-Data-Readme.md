In this folder, I have uploaded images that are intended to show how 
PyDist is more robust than DiANA. As we discussed, the fact that you
have to select how many pairs of objects to calculate centroid-centroid
distances should result in big differences in perceived colocalization
depending on how many objects are detected.

In inkscape, I made a picture in which a ball shaped object in channel 1
is surrounded by a large semicircle and three other objects ('Noisy_Centroid-Centroid_4obj.tif') 
in channel 2. I then made another image in which the semicirlce is divided into
two objects to make five objects in total ('Noisy_Centroid-Centroid_4obj.tif').
Each channel was exported as PNGs, converted to 16bit in imageJ, then noise was 
added as described in the 'Add_noise.py' file (located in the 'Generated Data Images' directory)

This data was processed in PyDist as described in the 'Generated Data PyDist Results'
directory. As shown in the 'PyDist_Generated_Data.csv' file, very little differences
between the two images are obsered (as expected). 

When trying to put this data into DiAna, I completely failed to get intelligable
results. I will continue to try to work this out, but would like some fresh 
eyes if possible. I have attached a macro that the lead author of DiAna sent 
me in 2018 which may help. 