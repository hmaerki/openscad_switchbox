from dataclasses import dataclass
from solid import *
from solid.utils import *

import library_box
import library_pcb
import library_display
import library_usb_switchbox_bottom

bottom = library_usb_switchbox_bottom.UsbSwitchBoxBottom()

@dataclass
class UsbSwitchBoxTop:
    size_y = bottom.size_y
    size_x = bottom.size_x
    size_z = 13
    hull_thickness = bottom.hull_thickness
    corner_r = bottom.corner_r
    screw_d = bottom.screw_d

    def draw(self):
        # Box with corners
        corner = library_box.Corner()
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

        pcb_offset_z = 29
        cores = translate(v=[0, 0, pcb_offset_z])(
            rotate([180, 0, 0])(
                library_usb_switchbox_bottom.UsbSwitchBoxCores(
                    size_x=self.size_x
                ).draw()
            )
        )

        return box_complete - cores


SEGMENTS = 100

box = UsbSwitchBoxTop()

scad_render_to_file(
    box.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
