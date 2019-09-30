"""test_integration_main.py

Integration tests

J. Metz <metz.jp@gmail.com>
"""
import numpy as np
import imageio
import scipy.ndimage as ndi
from pydist3d import main


def create_temp_image(tmp_path):
    """Utility to create temporary data"""
    image = np.random.rand(2, 100, 100)
    image = ndi.gaussian_filter(image, sigma=[0, 3, 3])
    image -= image.min()
    image /= image.max()
    image = (image > 0.6).astype('uint8')
    tempfile = tmp_path / "data.tif"
    imageio.volwrite(tempfile, image, format='tiff')
    return tempfile


def test_main(tmp_path):
    """Coarse-grained test that this thing runs properly"""
    imagefile = create_temp_image(tmp_path)
    output_folder = f"{imagefile.as_posix()}_output"
    main.main(imagefile.parent, output_folder)
