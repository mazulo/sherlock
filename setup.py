#!/usr/bin/env python

"""
Installer for sherlock.
"""

import sys
import unittest
from pathlib import Path

from setuptools import Command, find_packages, setup

from sherlock.sherlock import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


class TestCommand(Command):
    description = "Runs all available tests."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(tests)
        if not result.wasSuccessful():
            sys.exit(1)


setup(
    cmdclass={"test": TestCommand},
    name="sherlock-hunt",
    version=__version__,
    url="https://github.com/mazulo/sherlock",
    download_url=f"https://github.com/mazulo/sherlock/tarball/{__version__}",
    author="Patrick Mazulo",
    author_email="pmazulo@gmail.com",
    description="Sherlock: Find Usernames Across Social Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    entry_points={"console_scripts": ["sherlock = sherlock.sherlock:main"]},
    install_requires=[
        "certifi>=2019.6.16",
        "colorama>=0.4.1",
        "PySocks>=1.7.0",
        "requests>=2.28.1",
        "requests-futures>=1.0.0",
        "stem>=1.8.0 ",
        "torrequest>=0.1.0",
        "pandas>=1.0.0",
        "openpyxl<=3.0.10",
    ],
    keywords="cli, code, search, social media",
    license="MIT License",
    platforms=["POSIX"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)
