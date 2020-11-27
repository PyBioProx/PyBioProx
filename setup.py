#!/usr/bin/env python
"""setup.py

Setup script for pybioprox module

J. Metz <metz.jp@gmail.com>
"""
import os
from typing import List
import importlib
from setuptools import setup, Command


MODNAME = "pybioprox"


def create_cmdclass():
    """
    Adds coverage command class if coverage and pytest are available
    """
    try:
        importlib.import_module("coverage")
        importlib.import_module("pytest")
        return {
            "coverage": CoverageCommand
        }
    except ImportError:
        return {}


class CoverageCommand(Command):
    """Coverage Command"""
    description = "Run coverage on unit-tests (not integration tests!)"
    user_options: List = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):  # pylint: disable=no-self-use
        """runner"""
        # Coverage command
        # NOTE: Use API as follows for better control
        omitfiles = [
            os.path.join(MODNAME, "tests", "unit", "*"),
            os.path.join(MODNAME, "__main__.py"),
        ]
        for root, _, files in os.walk(MODNAME):
            omitfiles.extend(
                os.path.join(root, fname) for fname in
                filter(lambda f: f == "__init__.py", files)
            )
        coverage = importlib.import_module("coverage")
        pytest = importlib.import_module("pytest")

        print("Running coverage on", MODNAME)
        cov = coverage.Coverage(
            source=[MODNAME],
            omit=omitfiles,
            )
        cov.start()
        # Run normal tests
        # loader = unittest.TestLoader()
        # tests = loader.discover(MODNAME)
        # runner = unittest.runner.TextTestRunner()
        # runner.run(tests)
        pytest.main([])
        cov.save()
        cov.html_report()


setup(
    name=MODNAME,
    version='0.1',
    description='Distance-based colocalisation analysis module',
    author='Jeremy Metz',
    author_email='j.metz@exeter.ac.uk',
    packages=[MODNAME],
    test_suite=f"{MODNAME}.tests",
    setup_requires=['pytest-runner'],
    install_requires=[
        "imageio==2.6.1",
        "scipy==1.4.1",
        "scikit_image==0.16.2",
        "colorama==0.4.3",
        "coloredlogs==14.0",
        "pandas==1.0.3",
        "numpy>=1.18",
        "tifffile==2020.2.16",
        "matplotlib==3.2.1",
    ],
    tests_require=['pytest'],
    scripts=['pybioprox_gui.py'],
    cmdclass=create_cmdclass(),
)
