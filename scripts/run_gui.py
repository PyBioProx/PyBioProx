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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.threshold_options = ["None", "Otsu"]
        self.channel_1_options = ["0", "1", "2"]
        self.channel_2_options = ["0", "1", "2"]
        self.input_folder = None
        self.output_folder = None

        # self.resize(600, 480)
        self.setWindowTitle("PyDist3D Settings")

        select_input_label = QtWidgets.QLabel("Input folder", self)
        self.select_input_text = QtWidgets.QLineEdit(self)
        self.select_input_text.setReadOnly(True)
        select_input_button = QtWidgets.QPushButton("Select", self)
        select_input_button.clicked.connect(self.select_input)

        select_output_label = QtWidgets.QLabel("Output folder", self)
        self.select_output_text = QtWidgets.QLineEdit(self)
        self.select_output_text.setReadOnly(True)
        select_output_button = QtWidgets.QPushButton("Select", self)
        select_output_button.clicked.connect(self.select_output)

        select_threshold_label = QtWidgets.QLabel("Thresholding", self)
        self.select_threshold_select = QtWidgets.QComboBox(self)
        self.select_threshold_select.addItems(self.threshold_options)

        select_channel_1_label = QtWidgets.QLabel("Channel 1", self)
        self.select_channel_1 = QtWidgets.QComboBox(self)
        self.select_channel_1.addItems(self.channel_1_options)

        select_channel_2_label = QtWidgets.QLabel("Channel 2", self)
        self.select_channel_2 = QtWidgets.QComboBox(self)
        self.select_channel_2.addItems(self.channel_2_options)

        cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.run_button = QtWidgets.QPushButton("Run", self)
        self.run_button.setEnabled(False)
        cancel_button.clicked.connect(
            lambda: QtWidgets.QApplication.instance().exit(-1))
        self.run_button.clicked.connect(
            QtWidgets.QApplication.instance().quit)

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

        layout.addWidget(select_threshold_label, 3, 1)
        layout.addWidget(self.select_threshold_select, 3, 2, 1, 2)

        layout.addWidget(cancel_button, 5, 3)
        layout.addWidget(self.run_button, 5, 4)
        self.setLayout(layout)
        self.show()

    def select_input(self):
        self.input_folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select input data folder",
        )
        self.select_input_text.setText(self.input_folder)
        self.run_button.setEnabled(
            bool(self.input_folder and self.output_folder))


    def select_output(self):
        self.output_folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select output folder",
        )
        self.select_output_text.setText(self.output_folder)
        self.run_button.setEnabled(
            bool(self.input_folder and self.output_folder))

    def get_settings(self):
        return {
            "input_folder": self.input_folder,
            "output_folder": self.output_folder,
            "channel 1": self.select_channel_1.currentText(),
            "channel 2": self.select_channel_2.currentText(),
            "threshold_method": self.select_threshold_select.currentText(),
        }


def get_settings():
    """
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
        output_folder=settings["output_folder"]
    )


if __name__ == '__main__':
    main()
