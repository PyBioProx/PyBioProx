"""test_integration_main.py

Integration tests

Copyright (C) 2020  Jeremy Metz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
