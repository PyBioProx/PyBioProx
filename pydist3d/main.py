"""main.py

Main entry module for pydist3d

J. Metz <metz.jp@gmail.com>
"""
import os
import csv
import warnings
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import skimage.filters as skfilt
from pydist3d import distance_analysis
from pydist3d.utility import logger


# ------------------------------
# Add in calibration of pixels in xy and z directions
# ------------------------------
__zmicsperpix__ = 0.75
__xymicsperpix__ = 0.08


def get_files(folder):
    """
    find .tif files in input_folder_name, add to directory
    """
    listing = os.listdir(folder)
    filename_list = [
        os.path.join(folder, item)
        for item in listing if item.endswith(".tif")]
    return filename_list


def process_file(
        filepath,
        output_folder,
        distance_analyser='edge-to-edge'):
    """
    Perform main processing on the file
    """
    if isinstance(distance_analyser, str):
        distance_analyser = distance_analysis.get_analyser(distance_analyser)
    # load the data using tifffile, unlike when
    # loading .czi files, no unnecessary
    # dimensions are added, meaning that we do not need to
    # use the .squeeze function.
    datain = tifffile.imread(filepath)

    # Move channel axis to front
    data = shuffle_smallest_dim_to_front(datain)

    if data.ndim > 4:
        raise ValueError(
            "Unhandled dimensionality of data"
            + f"\nData must be 3-4 dimensional, got {data.ndim}")
    if data.ndim < 3:
        raise ValueError(
            "Input image must contain 2 channels and therefore"
            " be at least 3d")

    # split channels
    channel1 = data[0]
    channel2 = data[1]

    if channel1.ndim == 3:
        channel1 = shuffle_smallest_dim_to_front(channel1)
        channel2 = shuffle_smallest_dim_to_front(channel2)

    logger.debug("Channel 1 data has shape: %s", channel1.shape)
    logger.debug("Channel 2 data has shape: %s", channel2.shape)
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
    distances_list, dist_stats_list = distance_analyser(
        mask1, mask2,
        xymicsperpix=__xymicsperpix__, zmicsperpix=__zmicsperpix__)

    output_distances_and_stats(
        os.path.basename(filepath), output_folder,
        distances_list, dist_stats_list)


def output_distances_and_stats(name, folder, distances, dist_stats):
    """
    Outputs the distances and stats, for filename `name`
    into output folder `folder`
    """
    # Now that we have all the distances in a list, we could
    # perform statistical tests on them, or get their means,
    # maxima etc, but for now let's just write them to a
    # CSV (comma-seperated-values) file which can be loaded
    # into a variety of software (including Excel...) for
    # later inspection!

    if not os.path.isdir(folder):
        os.makedirs(folder)

    # To do this we're going to "open" a file (which returns
    # a "file-object" representing the open file
    # and then use the Python standard library's csv module
    # to send the data to the open file!
    file_out = open(os.path.join(folder, f"distance_table_{name}.csv"), "w")
    writer = csv.writer(file_out)
    writer.writerows(distances)
    file_out.close()

    file_out = open(os.path.join(folder, f"stats_table_{name}.csv"), "w")
    writer = csv.writer(file_out)
    writer.writerows(dist_stats)
    file_out.close()


def shuffle_smallest_dim_to_front(data):
    """
    Assumes smallest axis is channel axis and
    moves it to be the first dimension
    """
    channel_dim = np.argmin(data.shape)
    return np.moveaxis(data, channel_dim, 0)


def plot_and_save_outlines(channel1, channel2, mask1, mask2, filepath):
    """
    Creates and saves outline plots from the channel data and masks
    """
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
    if len(np.unique(mask1[slices])) > 1:
        plt.contour(mask1[slices], levels=[0.5], colors=["r"])
        savename = "{}_mask1.png".format(filepath)
    else:
        savename = "{}_mask1_NO_REGIONS.png".format(filepath)
    plt.savefig(savename)
    plt.close()

    # channel2 overlay images:
    plt.figure(
        "Mask 2",
        figsize=(12, 12 * size[0] / size[1]),
        dpi=size[1] / 12,
    )
    plt.axes([0, 0, 1, 1])
    plt.imshow(channel2[slices], cmap="gray")
    if len(np.unique(mask2[slices])) > 1:
        plt.contour(mask2[slices], levels=[0.5], colors=["r"])
        warnings.warn(f"Values in mask2[slices]: {np.unique(mask2[slices])}")
        savename = "{}_mask2.png".format(filepath)
    else:
        savename = "{}_mask2_NO_REGIONS.png".format(filepath)
    plt.savefig(savename)
    plt.close()
    logger.info("Created overlay images")


def batch(input_folder, output_folder):
    """
    Batch process all the data files in a given folder,
    saving results to the nominated `output_folder`.
    """
    filename_list = get_files(input_folder)

    for index, filepath in enumerate(filename_list):
        filename = os.path.basename(filepath)
        logger.info(
            "processing file %s, this is file %d of %d",
            filename, index + 1, len(filename_list))
        process_file(filepath, output_folder)


def main(input_folder, output_folder=None):
    """
    Main entry point to run the pydist3d analysis pipeline
    """
    if output_folder is None:
        output_folder = os.path.join(input_folder, "tables")
    batch(input_folder, output_folder)


def main_cli():
    """
    Main CLI interface
    """
    logger.debug("Running as script...")
    folder = input("Please enter an input folder")
    main(folder)


if __name__ == '__main__':
    main_cli()
