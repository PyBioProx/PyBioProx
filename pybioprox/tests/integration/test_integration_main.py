"""test_integration_main.py

Integration tests

J. Metz <metz.jp@gmail.com>
"""
import os
import numpy as np
import imageio
import scipy.ndimage as ndi
from pybioprox import main


def create_temp_image_simple(tmp_path):
    """Utility to create temporary data"""
    image = np.random.rand(2, 100, 100)
    image = ndi.gaussian_filter(image, sigma=[0, 3, 3])
    image -= image.min()
    image /= image.max()
    image = (image > 0.6).astype('uint8')
    tempfile = tmp_path / "data.tif"
    imageio.volwrite(tempfile, image, format='tiff')
    return tempfile


def create_temp_image_realistic(tmp_path):
    """Utility to create temporary data"""
    image = np.random.rand(2, 500, 500)
    image = ndi.gaussian_filter(image, sigma=[0, 3, 3])
    image -= image.min()
    image /= image.max()
    image = (image > 0.7).astype('uint8')
    tempfile = tmp_path / "data.tif"
    imageio.volwrite(tempfile, image, format='tiff')
    return tempfile


def test_main_simple(tmp_path):
    """Coarse-grained test that this thing runs properly"""
    imagefile = create_temp_image_simple(tmp_path)
    output_folder = f"{imagefile.as_posix()}_output"
    main.main(imagefile.parent, output_folder)
    # All we care about is having some output
    assert len(os.listdir(output_folder)) == 2


def test_main_realistic(tmp_path):
    """
    Coarse-grained test that this thing runs properly with more realistic data
    """
    imagefile = create_temp_image_realistic(tmp_path)
    output_folder = f"{imagefile.as_posix()}_output"
    main.main(imagefile.parent, output_folder)
    # Here we want to make sure we have non empty output
    assert len(os.listdir(output_folder)) == 2
    for output_file in os.listdir(output_folder):
        assert os.path.getsize(os.path.join(output_folder, output_file)) > 0
