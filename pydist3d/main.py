import os
import csv
import logging
import coloredlogs
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import skimage.filters as skfilt


logger = logging.getLogger(__name__)
# Default format for coloredlogs is
# "%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
coloredlogs.install(
    fmt="%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s",
    level='DEBUG', logger=logger
)


# ------------------------------
# Add in calibration of pixels in xy and z directions
# ------------------------------
zmicsperpix = 0.75
xymicsperpix = 0.08


def get_files(folder):
    # find .tif files in input_folder_name, add to directory
    listing = os.listdir(folder)
    filename_list = [
        os.path.join(folder, item)
        for item in listing if item.endswith(".tif")]
    return filename_list


def batch(input_folder, output_folder):
    """
    Batch process all the data files in a given folder,
    saving results to the nomincated `output_folder`.
    """
    filename_list = get_files(input_folder)

    for index, filepath in enumerate(filename_list):
        filename = os.path.basename(filepath)
        logger.info(
            "processing file{}, this is file {} of {}".format(
                filename, index + 1, len(filename_list)))
        process_file(filepath, output_folder)


def process_file(filepath, output_folder):
    """
    Perform main processing on the file
    """
    # load the data using tifffile, unlike when
    # loading .czi files, no unnecessary
    # dimensions are added, meaning that we do not need to
    # use the .squeeze function.
    filename = os.path.basename(filepath)
    datain = tifffile.imread(filepath)

    # Move channel axis to front
    data = shuffle_smallest_dim_to_front(datain)

    if data.ndim > 4:
        raise ValueError(
            "Unhandled dimensionality of data"
            + f"\nData must be 3-4 dimensional, got {data.ndim}")

    # split channels
    channel1 = data[0]
    channel2 = data[1]

    if channel1.ndim == 3:
        channel1 = shuffle_smallest_dim_to_front(channel1)
        channel2 = shuffle_smallest_dim_to_front(channel2)

    logger.debug(f"Channel 1 data has shape: {channel1.shape}")
    logger.debug(f"Channel 2 data has shape: {channel2.shape}")
    # at this point extra filtering steps can be inserted; I
    # have pre-filtered tis data in image-j so no need for extra filtering
    filtered1 = channel1
    filtered2 = channel2
    # identify thresholding values using threshold_otsu
    threshold_value1 = skfilt.threshold_otsu(filtered1)
    threshold_value2 = skfilt.threshold_otsu(filtered2)
    # apply threshold using comparison operator to generate 3D binary stacks
    mask1 = filtered1 >= threshold_value1
    mask2 = filtered2 >= threshold_value2

    # Generate distance map of mask2 - Note: because the distance
    # map here measures how far to the nearest OFF pixel (0), we need to
    # invert the mask while performing this function
    # Aside: the edt part of the function just stands for
    # Exact euclidean distance transform, as the module
    # also has other ways of calculating different
    # distance transforms!
    # NOTE: Includes pixel sampling factors;
    # so distances will be in microns
    sampling = [xymicsperpix for shape in channel1.shape]
    if len(sampling) == 3:
        sampling[0] = zmicsperpix

    distancemap2 = ndi.distance_transform_edt(~mask2, sampling=sampling)

    # We now create overlay figures for channel 1 and 2
    # and save to the input folder to allow
    # the thresholding to be assessed
    # Create a new figure object, and set the window title

    plot_and_save_outlines(
        channel1, channel2, mask1, mask2, filepath)

    # So next, for each object in mask1, let's
    # See how far it's border pixels are from the
    # nearest object in mask2 (using distancemap2)...

    # First we create a "labelled" array, which
    # performs part of what happens with
    # "Analyze particles" in imagej; it identifies
    # connected clumps of pixels and gives them all a unique
    # label.

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

    # Now that we have all the distances in a list, we could
    # perform statistical tests on them, or get their means,
    # maxima etc, but for now let's just write them to a
    # CSV (comma-seperated-values) file which can be loaded
    # into a variety of software (including Excel...) for
    # later inspection!

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    # To do this we're going to "open" a file (which returns
    # a "file-object" representing the open file
    # and then use the Python standard library's csv module
    # to send the data to the open file!
    file_out = open(os.path.join(
        output_folder, f"distance_table_{filename}.csv"), "w")
    writer = csv.writer(file_out)
    writer.writerows(distances_list)
    file_out.close()

    file_out = open(os.path.join(
        output_folder, f"stats_table_{filename}.csv"), "w")
    writer = csv.writer(file_out)
    writer.writerows(dist_stats_list)
    file_out.close()


def shuffle_smallest_dim_to_front(data):
    """
    Assumes smallest axis is channel axis and
    moves it to be the first dimension
    """
    channel_dim = np.argmin(data.shape)
    return np.moveaxis(data, channel_dim, 0)


def plot_and_save_outlines(channel1, channel2, mask1, mask2, filepath):
    # channel1 overlay images:
    size = channel1.shape[-2:]
    slices = [slice(None) for dim in channel1.shape]
    for i in range(channel1.ndim-2):
        # Get middle slice of any remaining channels
        middle_index = channel1.shape[i]//2
        slices[i] = middle_index
    slices = tuple(slices)

    plt.figure(
        "Mask 1",
        figsize=(12, 12 * size[0] / size[1]),
        dpi=size[1] / 12,
    )
    plt.axes([0, 0, 1, 1])
    plt.imshow(channel1[slices], cmap="gray")
    plt.contour(mask1[slices], levels=[0.5], colors=["r"])
    plt.savefig("{}_mask1.png".format(filepath))
    plt.close()

    # channel2 overlay images:
    plt.figure(
        "Mask 2",
        figsize=(12, 12 * size[0] / size[1]),
        dpi=size[1] / 12,
    )
    plt.axes([0, 0, 1, 1])
    plt.imshow(channel2[slices], cmap="gray")
    plt.contour(mask2[slices], levels=[0.5], colors=["r"])
    plt.savefig("{}_mask2.png".format(filepath))
    plt.close()
    logger.info("Created overlay images")


def main(input_folder, output_folder=None):
    """
    Main entry point to run the pydist3d analysis pipeline
    """
    if output_folder is None:
        output_folder = os.path.join(input_folder, "tables")
    batch(input_folder, output_folder)


if __name__ == '__main__':
    logger.debug("Running as script...")
    input_folder = input("Please enter an input folder")
    main(input_folder)
