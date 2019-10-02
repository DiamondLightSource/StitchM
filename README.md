# MosaicStitch
This was created to stitch together mosaic images taken in Cockpit (Micron)
into a universally readable format, currently '.ome.tiff'.

The current output is an 16bit greyscale image when stitching the mosaic.
Markers exported from Cockpit can be added as rectangular ROIs within the OME
metadata stored in the image header. ROIs can be imported and displayed using
bioformats in FIJI/ImageJ.

## Motivation
To make a mosaic image that can be easily viewed and can be used for automatic 
alignment with a separate grid image (using gridSNAP).

## Features
- [x] It works
- [x] Creates tiff from .txt file that links to a .mrc
- [x] Applies exposure compensation from file values
- [x] Slight exposure trimming to remove extreme highlights before normalisation
- [x] Image normalisation
- [x] OME-TIFF metadata
- [x] ROIs to show where data was taken (if markers used and exported)
- [x] .bat file processing

### Copyright

MosaicStitch is licensed under a BSD license, please see LICENSE file.
Copyright (c) 2019, Diamond Light Source Ltd. All rights reserved.

omexml.py is modified from python-bioformats, a part of CellProfiler. It is
also under a BSD license and can be found at
https://github.com/CellProfiler/python-bioformats

As Cockpit creates the images and accompanying files, so was referenced for the
creation of this software. Cockpit is licensed under GNU and can be found at
https://github.com/MicronOxford/cockpit
