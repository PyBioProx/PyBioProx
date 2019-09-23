"""distance_analysis.py

Distance analysis functions

J. Metz <metz.jp@gmail.com>
"""
import scipy.ndimage as ndi
from pydist3d.utility import logger


def analyse_distances_edge_edge(mask1, mask2, xymicsperpix=1, zmicsperpix=1):
    """
    Analyses edge-to-edge distances TODO: COMPLETE ME
    """
    # Generate distance map of mask2 - Note: because the distance
    # map here measures how far to the nearest OFF pixel (0), we need to
    # invert the mask while performing this function
    # Aside: the edt part of the function just stands for
    # Exact euclidean distance transform, as the module
    # also has other ways of calculating different
    # distance transforms!
    # NOTE: Includes pixel sampling factors;
    # so distances will be in microns
    sampling = [xymicsperpix for shape in mask1.shape]
    if len(sampling) == 3:
        sampling[0] = zmicsperpix
    distancemap2 = ndi.distance_transform_edt(~mask2, sampling=sampling)

    labels1, num_objects1 = ndi.label(mask1)

    if num_objects1 > 500:
        logger.critical(f"Too many objects found ({num_objects1}), skipping")
        return
    # NB: As this function is in scipy.ndimage - it happily handles
    # N-d data for us!
    # It also outputs the number of objects found, so we can show that
    # in the terminal...

    logger.info(f"Number of objects in mask1: {num_objects1}")

    # Next we want to process each labelled region (~object)
    # individually, so we will use a for-loop
    # We know how many objects there are from num_objects1

    # NOTE: The Python range function, when called with two inputs
    # generates the numbers input1, input1+1, input1+2, ... , input2-1
    # I.e. it does not generate input2, so if we want to have a
    # range of numbers go to X, then we have to use X+1 as the second input!

    # We're also going to create a list of distances - one
    # entry per object, but each entry itself is going to
    # be a list of distances!

    # First, let's create an empty list using []
    distances_list = []
    dist_stats_list = [
        [
            "min distance",
            "max distance",
            "mean distance",
            "median distance",
            "sum distance",
            "total number of bacterial perimiter pixels",
        ]
    ]

    for label in range(1, num_objects1 + 1):

        # Now we generate a mask of just this object
        # which is kind of like an ROI object in imagej
        # We can do this by using the comparison operator ==
        # which evaluates to true where values in labels1 are equal
        # to label
        mask_obj = labels1 == label

        # Now we can generate an outline of this region by performing
        # binary erosion of this region and getting the pixels where
        # mask_obj is True, but the eroded version is False!
        eroded = ndi.binary_erosion(mask_obj)
        outline = mask_obj & ~eroded

        # Now we can get all the distances of the outline pixels
        # to the nearest object in mask2!
        distances = distancemap2[outline]
        dist_arr = np.array(distances)
        dist_stats = [
            np.min(dist_arr),
            np.max(dist_arr),
            np.mean(dist_arr),
            np.median(dist_arr),
            np.sum(dist_arr),
            dist_arr.shape[0],
        ]
        # This uses "logical indexing", i.e. we can pass in a mask array
        # to extract only pixels in distancemap2 where the mask array
        # (in this case outline) is True.

        # Lastly we just need to decide what to do with the distances...
        # For now, let's create a table, so we're going to append the
        # current distances to the end of the list
        distances_list.append(distances)
        dist_stats_list.append(dist_stats)
    output_distances_and_stats(output_folder, distances_list, dist_stats_list)
