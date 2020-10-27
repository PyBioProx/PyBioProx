#!/usr/bin/env python
"""setup.py

Setup script for pybioprox module

J. Metz <metz.jp@gmail.com>
"""
import os
import unittest
from typing import List
from setuptools import setup, Command
# Coverage command
import coverage
import pytest

MODNAME = "pybioprox"


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
    tests_require=['pytest'],
    scripts=['pybioprox_gui.py'],
    cmdclass={
        "coverage": CoverageCommand,
    },
)
