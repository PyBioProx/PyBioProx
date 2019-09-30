"""test_main.py

Test main module

J. Metz <metz.jp@gmail.com>
"""
import os
import pytest
import numpy as np
from pydist3d import main


class TestMain:
    """
    Test main function
    """

    def test_missing_folder(self):
        with pytest.raises(FileNotFoundError):
            main.main(input_folder="i don't exist")

    def test_existing_folder_no_files(self, monkeypatch):
        called_batch = 0
        input_folder_junk = "doesn't matter"
        output_folder_junk = os.path.join(input_folder_junk, "tables")

        def mock_batch(input_folder, output_folder):
            nonlocal called_batch
            called_batch += 1
            assert input_folder == input_folder_junk
            assert output_folder == output_folder_junk

        monkeypatch.setattr(main, "batch", mock_batch)
        main.main(input_folder=input_folder_junk)
        assert called_batch == 1

    def test_existing_folder_no_data_files(self, monkeypatch):
        called_batch = 0
        input_folder_junk = "doesn't matter"
        output_folder_junk = os.path.join(input_folder_junk, "tables")

        def mock_batch(input_folder, output_folder):
            nonlocal called_batch
            called_batch += 1
            assert input_folder == input_folder_junk
            assert output_folder == output_folder_junk

        monkeypatch.setattr(main, "batch", mock_batch)
        main.main(input_folder=input_folder_junk)
        assert called_batch == 1


class TestBatch:
    """
    Test the batching function
    """
    def test_existing_folder_no_files(self, monkeypatch):
        called_get_files = 0
        called_process_file = 0
        folder_junk = "doesn't matter"
        folder_out_junk = os.path.join(folder_junk, "tables")

        def mock_get_files(arg):
            nonlocal called_get_files
            called_get_files += 1
            assert arg == folder_junk
            return []

        def mock_process_file(*args, **kwargs):
            nonlocal called_process_file
            called_process_file += 1

        monkeypatch.setattr(main, "get_files", mock_get_files)
        monkeypatch.setattr(main, "process_file", mock_process_file)
        main.batch(folder_junk, output_folder=folder_out_junk)
        assert called_get_files == 1
        assert called_process_file == 0


    def test_existing_folder_with_data(self, monkeypatch):
        called_get_files = 0
        called_process_file = 0
        folder_junk = "doesn't matter"
        folder_out_junk = os.path.join(folder_junk, "tables")
        data_files = ["a.tif", "b.tif", "c.tif"]

        def mock_get_files(arg):
            nonlocal called_get_files
            called_get_files += 1
            assert arg == folder_junk
            return data_files

        def mock_process_file(*args, **kwargs):
            nonlocal called_process_file
            called_process_file += 1

        monkeypatch.setattr(main, "get_files", mock_get_files)
        monkeypatch.setattr(main, "process_file", mock_process_file)
        main.batch(folder_junk, output_folder=folder_out_junk)
        assert called_get_files == 1
        assert called_process_file == 3




class TestGetFiles:
    def test_existing_folder_no_files(self, monkeypatch):
        called_os_listdir = 0
        folder_junk = "doesn't matter"

        def mock_os_listdir(arg):
            nonlocal called_os_listdir
            called_os_listdir += 1
            assert arg == folder_junk
            return []

        monkeypatch.setattr(os, "listdir", mock_os_listdir)
        main.get_files(folder_junk)
        assert called_os_listdir == 1

    def test_existing_folder_with_data(self, monkeypatch):
        called_os_listdir = 0
        folder_junk = "doesn't matter"
        data_files = ["a.tif", "b.tif", "c.tif"]
        all_files = data_files + ["something.txt"]

        def mock_os_listdir(arg):
            nonlocal called_os_listdir
            called_os_listdir += 1
            assert arg == folder_junk
            return all_files

        monkeypatch.setattr(os, "listdir", mock_os_listdir)
        value = main.get_files(folder_junk)
        assert called_os_listdir == 1
        assert value == [
            os.path.join(folder_junk, name) for name in data_files]


class TestProcessFile:
    def test_nonexistant_file(self, monkeypatch):
        called_imread = 0
        def mock_tifffile_imread_nonexistent(filename):
            nonlocal called_imread
            called_imread += 1
            raise FileNotFoundError(
                "FileNotFoundError: [Errno 2] No such file or directory:"
                + f" '{filename}'")
        monkeypatch.setattr(
            main.tifffile, 'imread', mock_tifffile_imread_nonexistent)
        with pytest.raises(FileNotFoundError):
            main.process_file(filepath="eggs.tif", output_folder="some_path")

    def test_with_only_2d_input_file(self, monkeypatch):
        called_imread = 0
        data = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])

        def mock_tifffile_imread(filename):
            nonlocal called_imread
            called_imread += 1
            return data

        monkeypatch.setattr(
            main.tifffile, 'imread', mock_tifffile_imread)

        with pytest.raises(ValueError):
            main.process_file(filepath="eggs.tif", output_folder="some_path")

    def test_with_3d_input_file(self, monkeypatch):
        called_imread = 0
        called_plottting_func = 0
        called_distance_analyser = 0
        data = np.array([
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]],
            [[9, 8, 7],
             [6, 5, 4],
             [3, 2, 1]]])

        def mock_tifffile_imread(filename):
            nonlocal called_imread
            called_imread += 1
            return data

        def mock_plotting_func(*args, **kwargs):
            nonlocal called_plottting_func
            called_plottting_func += 1

        def distance_analyser(*args, **kwargs):
            nonlocal called_distance_analyser
            called_distance_analyser += 1

        monkeypatch.setattr(
            main.tifffile, 'imread', mock_tifffile_imread)
        monkeypatch.setattr(
            main, 'plot_and_save_outlines', mock_plotting_func)

        main.process_file(
            filepath="eggs.tif",
            output_folder="some_path",
            distance_analyser=distance_analyser)
        assert called_imread == 1
        assert called_plottting_func == 1
        assert called_distance_analyser == 1
