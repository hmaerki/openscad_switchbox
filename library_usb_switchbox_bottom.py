from dataclasses import dataclass
from solid import *
from solid.utils import *

import library_box
import library_pcb
import library_display



@dataclass
class UsbSwitchBoxCores:
    size_x:float
    core_pcb_assembled = library_pcb.CorePcbAssembled()

    @property
    def core_pcb(self):
        return self.core_pcb_assembled.core_pcb

    def draw(self):
        pcb_offset_x = -8
        pcb_offset_z = 9

        cores = union()
        # Display
        display_x = self.size_x / 2
        display_z = 14
        cores += translate(v=[display_x, 0, display_z])(
            rotate([0, 0, 90])(library_display.CoreDisplay().draw())
        )
        # PCB
        cores += translate(v=[pcb_offset_x, 0, pcb_offset_z])(
            self.core_pcb_assembled.draw()
        )
        return debug(cores)

@dataclass
class Support:
    size_y: float
    size_z: float
    thickness_x = 2.0

    def draw(self):
        return translate(v=[0, 0, 0])(
            cube(
                size=[
                    self.thickness_x,
                    self.size_y,
                    self.size_z,
                ],
                center=True,
            )
        )


@dataclass
class UsbSwitchBoxBottom:
    size_y = 65
    size_x = 118
    size_z = 16
    hull_thickness = 2
    corner_r = 2.5
    screw_d = 3

    def draw(self):
        usb_switch_box_cores = UsbSwitchBoxCores(size_x=self.size_x)

        pcb_offset_x = -8
        pcb_offset_z = 9
        screws_distance_x = usb_switch_box_cores.core_pcb.screws_distance_x #  72 # Hack: Copied from library_pcb.py
        screws_distance_y = usb_switch_box_cores.core_pcb.screws_distance_y # 1.25 # Hack: Needs to be calculated correcty

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
        support = Support(size_y=self.size_y, size_z=self.size_z)
        display_supports_x = (14.0, 20.0)
        for x in display_supports_x:
            box_complete += (
                translate(
                    v=[
                        self.size_x / 2 - x - support.thickness_x / 2,
                        0,
                        self.size_z / 2,
                    ]
                )(support.draw()),
            )
        pcb_supports_x = (pcb_offset_x-screws_distance_x/2, pcb_offset_x+screws_distance_x/2)
        for x in pcb_supports_x:
            box_complete += (
                translate(
                    v=[
                        x,
                        screws_distance_y,
                        0,
                    ]
                )(debug(cylinder(h=pcb_offset_z, r=5))),
            )

        return box_complete - usb_switch_box_cores.draw()


SEGMENTS = 100

box = UsbSwitchBoxBottom()

scad_render_to_file(
    box.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
