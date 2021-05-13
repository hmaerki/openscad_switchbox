from dataclasses import dataclass
from solid import *
from solid.utils import *

import library_box
import library_pcb
import library_display


@dataclass
class UsbSwitchBox:
    size_y = 65
    size_x = 118
    size_z = 16
    hull_thickness = 2
    corner_r = 2.5
    screw_d = 3

    def draw(self):
        display_y = self.hull_thickness - self.size_x / 2
        display_z = 14
        display_support_width = 2.0
        display_support1_y = 14.0
        display_support2_y = 20.0

        pcb_offset_x = -8
        pcb_offset_z = 8

        corner = library_box.Corner()
        boxskeleton = library_box.BoxSkeleton(
            size_x=self.size_x,
            size_y=self.size_y,
            size_z=self.size_z,
            wall_thickness=self.hull_thickness,
        )
        box = library_box.Box(boxskeleton=boxskeleton, corner=corner)

        # The tray of the housing:
        d = difference()(
            union()(
                box.draw(),
                translate(
                    v=[-display_y - display_support1_y, -self.size_y / 2, 0]
                )(
                    cube(
                        size=[
                            display_support_width,
                            self.size_y,
                            self.size_z,
                        ]
                    )
                ),
                translate(
                    v=[-display_y - display_support2_y, -self.size_y / 2, 0]
                )(
                    cube(
                        size=[
                            display_support_width,
                            self.size_y,
                            self.size_z,
                        ]
                    )
                ),
            ),
            debug(
                union()(
                    # Display
                    translate(v=[self.size_x / 2, 0, display_z])(
                        rotate([0, 0, 90])(library_display.CoreDisplay().draw())
                    ),
                    # PCB
                    translate(v=[pcb_offset_x, 0, pcb_offset_z])(library_pcb.CorePcbAssembled().draw()),
                )
            ),
        )
        return d


SEGMENTS = 100

core_display = UsbSwitchBox()

scad_render_to_file(
    core_display.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
