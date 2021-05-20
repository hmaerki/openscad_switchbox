from dataclasses import dataclass
from solid import *
from solid.utils import *

import library_box
import library_usb_switchbox_bottom

bottom = library_usb_switchbox_bottom.UsbSwitchBoxBottom(is_top=False)


@dataclass
class UsbSwitchBoxTop:
    size_y = bottom.size_y
    size_x = bottom.size_x
    size_z_overall = 30
    size_z = size_z_overall - bottom.size_z
    hull_thickness = bottom.hull_thickness
    corner_r = bottom.corner_r
    screw_hole_top_d  = bottom.screw_hole_top_d    

    def draw(self):
        # Box with corners
        corner = library_box.Corner(hole_d=self.screw_hole_top_d)
        boxskeleton = library_box.BoxSkeleton(
            size_x=self.size_x,
            size_y=self.size_y,
            size_z=self.size_z,
            hull_thickness=self.hull_thickness,
        )
        box = library_box.Box(boxskeleton=boxskeleton, corner=corner)

        # Box with supports
        box_complete = union()
        box_complete += box.draw()

        support = library_usb_switchbox_bottom.SupportY(size_y=self.size_y, size_z=self.size_z)
        display_supports_x = (11.0, 19.3)
        for x in display_supports_x:
            box_complete += (
                translate(
                    v=[
                        self.size_x / 2 - x - support.thickness_x / 2,
                        0,
                        support.size_z / 2,
                    ]
                )(support.draw()),
            )

        pcb_offset_z = 29
        cores = translate(v=[0, 0, pcb_offset_z])(
            rotate([180, 0, 0])(
                library_usb_switchbox_bottom.UsbSwitchBoxCores(
                    size_x=self.size_x,
                    is_top=True
                ).draw()
            )
        )

        return box_complete - cores


SEGMENTS = 100

box = UsbSwitchBoxTop()

scad_render_to_file(
    box.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
