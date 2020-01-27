# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 11:16:04 2020

@author: jdeed
"""
import tifffile
import matplotlib.pyplot as plt
import numpy as np
#read image and select by channel
img = tifffile.imread(r'C:/Users/jdeed/OneDrive - University of Exeter/PyDist3D/Generated Data/Centroid-Centroid 5obj No Noise.tif')
channel1= img[0]
channel2 = img[1]

# add noise
noisychannel1 = channel1 + 1 * channel1.std() * np.random.random(channel1.shape)
noisychannel2 = channel2 + 1 * channel1.std() * np.random.random(channel1.shape)
noisyimg = img + 1 * img.std() * np.random.random(img.shape)

"""
#display images for comparison
print(img.shape)
originalchannel1 = img[0]
originalchannel2 = img[1]
imgplot = plt.imshow(originalchannel1,cmap = "Greys")
plt.show()
imgplot = plt.imshow(originalchannel2,cmap = "Greys")
plt.show()
imgplot = plt.imshow(noisychannel1,cmap = "Greys")
plt.show()
imgplot = plt.imshow(noisychannel2,cmap = "Greys")
plt.show()
"""
# for some reason, saving the 'noisyimg' object as a tif using tifffile.imsave
# resulted in a 64bit image, couldn't figure out why, so decided to 
# save each channel individually as a tif using plt.imsave,
# shove it into imageJ, merge channels and resave as a tif with a 16bit depth. 
plt.imsave('C:/Users/jdeed/OneDrive - University of Exeter/PyDist3D/Generated Data/data/Noisy channel 1 Centroid Test 5 Objects.tif', noisychannel1)
plt.imsave('C:/Users/jdeed/OneDrive - University of Exeter/PyDist3D/Generated Data/data/Noisy channel 2 Centroid Test 5 Objects.tif', noisychannel2)