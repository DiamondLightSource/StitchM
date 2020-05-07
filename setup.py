import os
import setuptools

from stitch_m import __version__, __author__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements=[
    "tifffile",
    "mrcfile",
    "numpy",
    "omexml-dls",
    "pywin32;platform_system=='Windows'"
    ]

setuptools.setup(
    name="StitchM",
    version=__version__,
    author=__author__,
    author_email="thomas.fish@diamond.ac.uk",
    description="A package for stitching mosaics from Cockpit with (or without) ROIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_file="LICENSE",
    url="https://github.com/DiamondLightSource/StitchM",
    install_requires=requirements,
    packages=setuptools.find_packages(exclude=("test", "scripts")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_data={'stitch_m': ['config.cfg', 'scripts/dragndrop.bat']},
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            "StitchM = stitch_m.scripts.command_line:cl_run"
            ]
            },
)
