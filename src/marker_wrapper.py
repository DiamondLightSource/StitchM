import numpy as np
import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from image_edge_definer import edge_definer


class Marker():

    def __init__(self, markerfile, img_params):
        self.boundaries = img_params["mosaic_boundaries"]
        self.centre = img_params["mosaic_centre"]
        self.pix2edge = img_params["pixels_to_edge"]
        self.pixelsize = img_params["pixel_size"]
        self.markerlist = self.extract_markers(markerfile)

    @staticmethod
    def is_marker_file(arg):
        pattern = re.compile(r'(.*)marker(.*).txt$', flags=re.I)
        if pattern.match(arg):
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
        markernum = 1
        annotations = Image.new('RGBA', mosaic.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(annotations, mode='RGBA')
        src_path = Path(__file__).resolve()
        fnt = ImageFont.truetype(str(src_path.with_name("Waukegan LDO.ttf")), size=300)
        for marker in self.markerlist:
            start, end = edge_definer(
                marker,
                self.boundaries,
                self.pix2edge
                )
            text_loc = [loc + (self.pix2edge[0] // 4) for loc in start]
            d.rectangle((start, end), fill=None, outline="red", width=15)
            d.text(text_loc, str(markernum), font=fnt, fill="red")
            markernum += 1
        assert(mosaic.size == annotations.size)
        im_out = Image.alpha_composite(mosaic, annotations)
        return im_out

