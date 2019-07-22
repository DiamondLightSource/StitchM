import numpy as np
import logging
import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from edge_definer import marker_edge_definer


class Marker():

    def __init__(self, markerfile, img_params):
        self.boundaries = img_params["mosaic_boundaries"]
        self.centre = img_params["mosaic_centre"]
        self.pix2edge = img_params["pixels_to_edge"]
        self.pixelsize = img_params["pixel_size"]
        self.markerlist = self.extract_markers(markerfile)

    @staticmethod
    def is_marker_file(arg):
        if re.match(r'(.*)marker(.*).txt$', arg, flags=re.I):
            return True
        else:
            return False

    def extract_markers(self, markerfile):
        # returns marker coordinates in pixels
        array = np.genfromtxt(markerfile, delimiter=",")
        marker_coordinates = []
        for marker_number in range(len(array[:, 0])):
            x, y = array[marker_number, 0:2]
            # x is flipped between image and marker coordinates
            x = ((-x - self.centre[0]) / self.pixelsize)
            y = ((y - self.centre[1]) / self.pixelsize)
            marker_coordinates.append((int(x), int(y)))
        return marker_coordinates

    def output_markers(self, mosaic):
        logging.debug("Creating marker layer")
        markernum = 1
        annotations = Image.new('RGBA', mosaic.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(annotations, mode='RGBA')
        src_path = Path(__file__).resolve()
        fnt = ImageFont.truetype(str(src_path.with_name("Waukegan LDO.ttf")), size=300)
        for marker in self.markerlist:
            start, end = marker_edge_definer(
                marker,
                self.boundaries,
                self.pix2edge
                )
            text_loc = (start[0] + (self.pix2edge[0] // 4), start[1] + (self.pix2edge[1] // 4))
            d.rectangle((start, end), fill=None, outline=(0, 255, 0, 255), width=20)
            d.text(text_loc, str(markernum), font=fnt, fill=(0, 255, 0, 255))
            markernum += 1
        im_out = Image.alpha_composite(mosaic, annotations)
        logging.debug("Marker image created")
        return im_out

