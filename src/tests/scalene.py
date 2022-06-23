"""
For running using Scalene (https://github.com/plasma-umass/scalene)

Run with:
`scalene src/tests/scalene.py` for just the overall stats
move scalene.py to the top level and run with `scalene scalene.py` for finer detail
"""
 
from os import path, remove
from pathlib import Path

from stitch_m import stitch_and_save

base_path = Path("/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files")
test_files = (
    base_path / "B15Grid2.txt",
    base_path / "B8G1-IR_mosaic.txt",
    base_path / "B8G2-IR_mosaic.txt",
    base_path / "Fid_T2G3_mosaic.txt",
    base_path / "Yo10_G3_mosaic.txt",
    base_path / "PP4_G2_mosaic.txt"
    )

test_marker_files = (
    base_path / "B15_location_markers.txt",
    base_path / "B8G1-IR_markers.txt",
    base_path / "B8G2-IR_markers.txt",
    base_path / "Fid_T2G3_markers.txt",
    base_path / "Yo10_G3_mosaic_MARKERS.txt",
    base_path / "PP4_G2_markers.txt"
    )

for mos, mar in zip(test_files, test_marker_files):
    stitch_and_save(mos, mar)
    output_path = str(mos).replace('.txt', '_marked.ome.tiff')

    if path.isfile(output_path):
        remove(output_path)
 