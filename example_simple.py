import pathlib
from solid import *

d = difference()(
    cube(10),
    sphere(15)
)
print(scad_render(d))


FILENAME_SCAD = pathlib.Path(__file__).with_suffix(".scad")
scad_render_to_file(d, FILENAME_SCAD)
