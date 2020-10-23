"""run_gui.py

Script to launch pybioprox and collect
any user input using GUI interfaces

J. Metz <metz.jp@gmail.com>
"""
import os
import sys
from dataclasses import make_dataclass, asdict
from PyQt5 import QtWidgets  # type: ignore
from pybioprox import main as pybioprox_main
import matplotlib.pyplot as plt
plt.switch_backend('qt5agg')


class PyDist3dSettingsWidget(QtWidgets.QWidget):
    """
    Class representing a dialog for inputting more advanced settings than just
    requesting the input folder name
    """
    # pylint: disable=c-extension-no-member
    # PyQt is full of these, so disabling globally for the class makes sense
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.resize(600, 480)
        self.select_input_text = None
        self.select_output_text = None
        self.select_filter_select = None
        self.select_threshold_select = None
        self.select_channel_1 = None
        self.select_channel_2 = None
        self.run_button = None
        self.generate_controls()
        self.generate_layout()
        self.setWindowTitle("PyDist3D Settings")
        self.show()

    def generate_controls(self):
        """
        Adds controls
        """
        threshold_options = ["None", "Otsu", "Li"]
        filter_options = ["None", "Gaussian (sigma 3px)"]
        channel_1_options = ["1", "2", "3"]
        channel_2_options = ["1", "2", "3"]
        self.select_input_text = QtWidgets.QLineEdit(self)
        self.select_input_text.setReadOnly(True)
        self.select_output_text = QtWidgets.QLineEdit(self)
        self.select_output_text.setReadOnly(True)
        self.select_filter_select = QtWidgets.QComboBox(self)
        self.select_filter_select.addItems(filter_options)
        self.select_threshold_select = QtWidgets.QComboBox(self)
        self.select_threshold_select.addItems(threshold_options)
        self.select_channel_1 = QtWidgets.QComboBox(self)
        self.select_channel_1.addItems(channel_1_options)
        self.select_channel_2 = QtWidgets.QComboBox(self)
        self.select_channel_2.addItems(channel_2_options)
        self.select_channel_2.setCurrentIndex(1)
        self.preview_button = QtWidgets.QPushButton("Preview", self)
        self.preview_button.setEnabled(False)
        self.preview_button.clicked.connect(self.run_preview)
        self.run_button = QtWidgets.QPushButton("Run", self)
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.do_run)

    def generate_layout(self):
        """
        Generates the layout
        """
        select_input_label = QtWidgets.QLabel("Input folder", self)
        select_input_button = QtWidgets.QPushButton("Select", self)
        select_input_button.clicked.connect(self.select_input)

        select_output_label = QtWidgets.QLabel("Output folder", self)
        select_output_button = QtWidgets.QPushButton("Select", self)
        select_output_button.clicked.connect(self.select_output)

        select_filter_label = QtWidgets.QLabel("Filtering", self)

        select_threshold_label = QtWidgets.QLabel("Thresholding", self)

        select_channel_1_label = QtWidgets.QLabel("Channel 1", self)

        select_channel_2_label = QtWidgets.QLabel("Channel 2", self)

        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(
            lambda: QtWidgets.QApplication.instance().exit(-1))

        layout = QtWidgets.QGridLayout()
        layout.addWidget(select_input_label, 0, 0)
        layout.addWidget(self.select_input_text, 0, 1, 1, 3)
        layout.addWidget(select_input_button, 0, 4)

        layout.addWidget(select_output_label, 1, 0)
        layout.addWidget(self.select_output_text, 1, 1, 1, 3)
        layout.addWidget(select_output_button, 1, 4)

        layout.addWidget(select_channel_1_label, 2, 0)
        layout.addWidget(self.select_channel_1, 2, 1)

        layout.addWidget(select_channel_2_label, 2, 2)
        layout.addWidget(self.select_channel_2, 2, 3)

        layout.addWidget(select_filter_label, 3, 1)
        layout.addWidget(self.select_filter_select, 3, 2, 1, 2)

        layout.addWidget(select_threshold_label, 4, 1)
        layout.addWidget(self.select_threshold_select, 4, 2, 1, 2)

        layout.addWidget(cancel_button, 5, 2)
        layout.addWidget(self.preview_button, 5, 3)
        layout.addWidget(self.run_button, 5, 4)
        self.setLayout(layout)

    def select_input(self):
        """
        Select the input folder using a standard Qt Dialog.
        Also then conditionally sets the run button as enabled
        """
        input_folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select input data folder",
        )
        output_folder = self.select_output_text.text()
        self.select_input_text.setText(input_folder)

        can_run = bool(input_folder and output_folder)
        self.run_button.setEnabled(can_run)
        self.preview_button.setEnabled(bool(input_folder))

    def select_output(self):
        """
        Select the output folder using a standard Qt Dialog.
        Also then conditionally sets the run button as enabled
        """
        input_folder = self.select_input_text.text()
        output_folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select output folder",
        )
        self.select_output_text.setText(output_folder)
        can_run = bool(input_folder and output_folder)
        self.run_button.setEnabled(can_run)

    def get_settings(self):
        """
        Return the settings as a dictionary
        """
        settings = {
            "input_folder": self.select_input_text.text(),
            "output_folder": self.select_output_text.text(),
            "channel1_index": int(self.select_channel_1.currentText())-1,
            "channel2_index": int(self.select_channel_2.currentText())-1,
            "filter_method": self.select_filter_select.currentText(),
            "threshold_method": self.select_threshold_select.currentText(),
        }
        return make_dataclass(
            "Settings", settings.keys(), frozen=True)(**settings)

    def do_run(self):
        """
        Perform validation - if all good, quit the application with
        the correct code for continuing with running
        """
        problem = self.is_problem_with_options()
        if problem:
            self.show_problem(*problem)
        else:
            QtWidgets.QApplication.instance().quit()

    def show_problem(self, problem_title, problem):
        """
        Shows a simple message box with a warning symbol
        """
        message = QtWidgets.QMessageBox(self)
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setText(problem_title)
        message.setInformativeText(problem)
        message.exec_()

    def is_problem_with_options(self):
        """
        Return message explaining problem with options if there is one
        or False if not
        """
        settings = self.get_settings()
        if not os.path.isdir(settings.input_folder):
            return (
                "Input folder problem",
                f"Input folder [{settings.input_folder}]"
                " must be an existing folder")
        if not os.path.isdir(settings.output_folder):
            return (
                "Output folder problem",
                f"Output folder [{settings.output_folder}]"
                " must be an existing folder")
        if settings.channel1_index == settings.channel2_index:
            return (
                "Channel selection problem",
                f"channel 1 [{settings.channel_1}]"
                f" must be diffent from channel 2 [{settings.channel_2}]")
        return False

    def run_preview(self):
        """Creates a preview of the current settings on the first file"""
        settings = asdict(self.get_settings())

        input_folder = settings.pop('input_folder')
        settings.pop('output_folder')
        config = pybioprox_main.Config(**settings)
        filename_list = pybioprox_main.get_files(input_folder)

        filepath = filename_list[0]

        channel1, channel2 = pybioprox_main.load_data(
            filepath, config.channel1_index, config.channel2_index)
        mask1, mask2 = pybioprox_main.detect_objects(
            channel1, channel2, config)

        pybioprox_main.plot_outlines(
            channel1, channel2, mask1, mask2)
        plt.show(block=False)
        # plt.figure()
        # plt.subplot(1, 2, 1)
        # plt.imshow(channel1, cmap='gray')
        # plt.imshow(mask
        # plt.subplot(1, 2, 2)
        # plt.imshow(1, 2, 2)
        # plt.show()


def get_settings():
    """
    Create and run the Settings dialog, returning the
    settings entered by the user
    """
    # pylint: disable=c-extension-no-member
    app = QtWidgets.QApplication([])
    window = PyDist3dSettingsWidget()
    return_code = app.exec_()
    if return_code != 0:
        print("Run cancelled, quitting")
        sys.exit()
    settings = window.get_settings()
    return settings


def main():
    """
    Main entry point function
    """
    settings = get_settings()
    print("Settings:", settings)
    pybioprox_main.main(**asdict(settings))


if __name__ == '__main__':
    main()
