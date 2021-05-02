# -*- coding: utf-8 -*-
"""
"""
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

INSTALL_REQUIRES = ["boto3==1.17.62", "click==7.1.2"]
CLASSIFIERS = []

ENTRY_POINTS = {
    "console_scripts": ["dougs_valheim_server = dougs_valheim_server.cli:cli"]
}

setup(
    name="dougs-valheim-server",
    version="0.1.0",
    description="Utility to start/stop my valheim server on AWS.",
    url="https://github.com/dougthor42/dougs-valheim-server",
    author="Douglas Thor",
    author_email="doug.thor@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=False,
    entry_points=ENTRY_POINTS,
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
)
