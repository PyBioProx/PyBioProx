"""run_gui.py

Script to launch pydist3d and collect
any user input using GUI interfaces

J. Metz <metz.jp@gmail.com>
"""
import os
import sys
import importlib
from PyQt5 import QtWidgets  # type: ignore

try:
    # pylint: disable=invalid-name
    pydist3d_main = importlib.import_module('pydist3d.main')
except ModuleNotFoundError:
    MODULE_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, MODULE_ROOT)
    # pylint: disable=invalid-name
    pydist3d_main = importlib.import_module('pydist3d.main')


def get_folder_gui(caption="Select folder"):
    """
    Use PyQt5 to get folder needed
    """
    # pylint: disable=c-extension-no-member
    _ = QtWidgets.QApplication([])
    folder = QtWidgets.QFileDialog.getExistingDirectory(
        parent=None,
        caption=caption
    )
    # pylint: enable=c-extension-no-member
    return folder


def main():
    """
    Main entry point function
    """
    folder = get_folder_gui("Select input folder")
    output_folder = get_folder_gui(
        "Select output folder or press cancel for default")
    if not output_folder:
        output_folder = None
    pydist3d_main.main(folder, output_folder=output_folder)


if __name__ == '__main__':
    main()
