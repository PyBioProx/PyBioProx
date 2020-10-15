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

        layout.addWidget(cancel_button, 5, 3)
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
        self.run_button.setEnabled(
            bool(input_folder and output_folder))

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
        self.run_button.setEnabled(bool(input_folder and output_folder))

    def get_settings(self):
        """
        Return the settings as a dictionary
        """
        return {
            "input_folder": self.select_input_text.text(),
            "output_folder": self.select_output_text.text(),
            "channel_1": int(self.select_channel_1.currentText())-1,
            "channel_2": int(self.select_channel_2.currentText())-1,
            "filter_method": self.select_filter_select.currentText(),
            "threshold_method": self.select_threshold_select.currentText(),
        }

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
        if not os.path.isdir(settings["input_folder"]):
            return (
                "Input folder problem",
                f"Input folder [{settings['input_folder']}]"
                " must be an existing folder")
        if not os.path.isdir(settings["output_folder"]):
            return (
                "Output folder problem",
                f"Output folder [{settings['output_folder']}]"
                " must be an existing folder")
        if settings["channel_1"] == settings["channel_2"]:
            return (
                "Channel selection problem",
                f"channel 1 [{settings['channel_1']}]"
                f" must be diffent from channel 2 [{settings['channel_2']}]")
        return False


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
    pydist3d_main.main(
        settings["input_folder"],
        output_folder=settings["output_folder"],
        channel1_index=settings["channel_1"],
        channel2_index=settings["channel_2"],
        filter_method=settings["filter_method"],
        threshold_method=settings["threshold_method"],
    )


if __name__ == '__main__':
    main()
