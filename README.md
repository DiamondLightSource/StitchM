# MosaicStitch
This was created to stitch together mosaic images taken in Cockpit (Micron) into a universally readable format, currently .tiff.

The current output is an 8bit grayscale image when stitching the mosaic. In order to show an the marked regions, the image had to be exported in RGB with two layers (one with and one without the markers) to allow colour annotations and image matching without the annotations.

## Motivation
To make a mosaic image that can be easily viewed and can be used for automatic alignment with a separate grid image (using gridSNAP).

## Features
- [x] Working
- [x] Creates tiff from .txt file that links to a .mrc
- [x] Improved automatic exposure compensation
- [x] Exposure trimming to remove extreme highlights before normalisation
- [x] Image normalisation
- [x] Can add a tiff layer to show where microscopy data was taken.
- [x] .bat file processing

### Copyright

As Cockpit creates the images and accompanying files, so was referenced for the creation of this software. Cockpit can be found at "https://github.com/MicronOxford/cockpit".

"Waukegan LDO" is a font created by Luke Owens (LILongJr@HotPOP.com), licensed as Freeware. It was downloaded from www.fontspace.com.