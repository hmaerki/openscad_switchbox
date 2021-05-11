from dataclasses import dataclass
from solid import scad_render_to_file


from library_box import Corner, Box

box = Box(corner=Corner(d=9, hole_xy=7))

SEGMENTS = 48

scad_render_to_file(
    box.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
