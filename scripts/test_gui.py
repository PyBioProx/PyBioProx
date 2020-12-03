"""test_gui.py

Gui testing script

J. Metz
"""
# import unittest
import sys
import os
try:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from pybioprox_gui import PyBioProxSettingsWidget, QtWidgets
except ImportError:
    print("Could not import gui module, please check location and try again")
    raise
from PyQt5 import QtCore


# class TestGui(unittest.TestCase):
#    def test_create(self, qtbot):
#        window = PyBioProxSettingsWidget()
#        qtbot.addWidget(window)
#        assert isinstance(window, PyBioProxSettingsWidget)

def test_create(qtbot):
    """
    Test creating a window
    """
    window = PyBioProxSettingsWidget()
    qtbot.addWidget(window)
    assert isinstance(window, PyBioProxSettingsWidget)


def test_run_disabled(qtbot):
    """
    Make sure run is disabled by default
    """
    window = PyBioProxSettingsWidget()
    qtbot.addWidget(window)
    assert not window.run_button.isEnabled()


def select_input_and_output_folders(window, tmpdir, monkeypatch):
    """
    Utility function to select input and output folders
    """
    input_folder = tmpdir.mkdir('input')
    output_folder = tmpdir.mkdir('output')

    # pylint: disable=c-extension-no-member
    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: str(input_folder))

    window.select_input_widget.select_folder()

    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: str(output_folder))

    window.select_output_widget.select_folder()
    return str(input_folder), str(output_folder)


def test_select_folder(qtbot, tmpdir, monkeypatch):
    """
    Test that folders can be selected, and that then the run button
    enables
    """
    window = PyBioProxSettingsWidget()
    qtbot.addWidget(window)
    select_input_and_output_folders(window, tmpdir, monkeypatch)
    assert window.run_button.isEnabled()


def test_run(qtbot, tmpdir, monkeypatch):  # , mocker):
    """
    Test that once the input and output folders are selected, that
    the result of get_settings makes sense
    """
    window = PyBioProxSettingsWidget()
    qtbot.addWidget(window)
    input_folder, output_folder = select_input_and_output_folders(
        window, tmpdir, monkeypatch)
    assert window.run_button.isEnabled()
    settings = window.get_settings()
    assert settings.input_folder == input_folder
    assert settings.output_folder == output_folder
    # pylint: disable=c-extension-no-member
    qtbot.mouseClick(window.run_button, QtCore.Qt.LeftButton)
