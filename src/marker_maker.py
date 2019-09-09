import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

import logger
from edge_definer import marker_edge_definer


class Marker():

    def __init__(self, markerfile, img_params):
        self.boundaries = img_params["mosaic_boundaries"]
        self.centre = img_params["mosaic_centre"]
        self.pix2edge = img_params["pixels_to_edge"]
        self.pixelsize = img_params["pixel_size"]
        self.markerlist, self.marker_numbers = self.extract_markers(markerfile)

    def extract_markers(self, markerfile):
        # returns marker coordinates in pixels
        array = np.genfromtxt(markerfile, delimiter=",")
        marker_coordinates = []
        marker_numbers = []
        for count in range(len(array[:, 0])):
            x, y = array[count, 0:2]
            # x is flipped between image and marker coordinates
            x = ((-x - self.centre[0]) / self.pixelsize)
            y = ((y - self.centre[1]) / self.pixelsize)
            marker_coordinates.append((int(x), int(y)))
            marker_numbers.append(int(array[count, -1]))
        return marker_coordinates, marker_numbers

    def output_markers(self, mosaic):
        logging.info("Creating marker layer")

        cross_size = self.pix2edge[0] // 3.5

        annotations = Image.new('RGBA', mosaic.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(annotations, mode='RGBA')
        src_path = Path(__file__).resolve()
        fnt = ImageFont.truetype(str(src_path.with_name("Waukegan LDO.ttf")), size=self.pix2edge[0])
        for count in range(len(self.marker_numbers)):
            start, end = marker_edge_definer(
                self.markerlist[count],
                self.boundaries,
                self.pix2edge
                )
            d.rectangle((start, end), fill=None, outline=(0, 255, 0, 255), width=20)

            text_loc = (start[0] + (self.pix2edge[0] // 6), start[1] + (self.pix2edge[1] // 6))
            d.text(text_loc, str(self.marker_numbers[count]), font=fnt, fill=(0, 255, 0, 255))

            cross_loc = (start[0] + self.pix2edge[0], start[1] + self.pix2edge[1])
            d.line([(cross_loc[0] + cross_size, cross_loc[1]), (cross_loc[0] - cross_size, cross_loc[1])], fill=(0, 255, 0, 255), width=15)
            d.line([(cross_loc[0], cross_loc[1] + cross_size), (cross_loc[0], cross_loc[1] - cross_size)], fill=(0, 255, 0, 255), width=15)

        im_out = Image.alpha_composite(mosaic, annotations)
        logging.info("Marker image created")
        return im_out

