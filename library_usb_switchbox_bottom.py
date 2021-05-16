from dataclasses import dataclass
from solid import *
from solid.utils import *

import library_box
import library_pcb
import library_display

SMALL = 0.0001


@dataclass
class UsbSwitchBoxCores:
    size_x: float
    core_pcb_assembled = library_pcb.CorePcbAssembled()
    pcb_offset_x = -6
    pcb_offset_z = 9

    @property
    def core_pcb(self):
        return self.core_pcb_assembled.core_pcb

    def draw(self):
        cores = union()
        # Display
        display_x = self.size_x / 2
        display_z = 14
        cores += translate(v=[display_x, 0, display_z])(
            rotate([0, 0, 90])(library_display.CoreDisplay().draw())
        )
        # PCB
        cores += translate(v=[self.pcb_offset_x, 0, self.pcb_offset_z])(
            self.core_pcb_assembled.draw()
        )
        return debug(cores)


@dataclass
class SupportY:
    size_y: float
    size_z: float
    thickness_x = 1.6

    def draw(self):
        return cube(
            size=[
                self.thickness_x,
                self.size_y,
                self.size_z,
            ],
            center=True,
        )


@dataclass
class SupportX:
    size_x: float
    size_z: float
    thickness_y = 1.6

    def draw(self):
        return cube(
            size=[
                self.size_x,
                self.thickness_y,
                self.size_z,
            ],
            center=True,
        )


@dataclass
class UsbSwitchBoxBottom:
    size_y = 65
    size_x = 120
    size_z = 16.5
    hull_thickness = 1.6
    corner_r = 2.5
    screw_d = 3

    def draw(self):
        usb_switch_box_cores = UsbSwitchBoxCores(size_x=self.size_x)

        pcb_offset_x = usb_switch_box_cores.pcb_offset_x
        pcb_offset_z = usb_switch_box_cores.pcb_offset_z
        screws_distance_x = usb_switch_box_cores.core_pcb.screws_distance_x
        screws_distance_y = usb_switch_box_cores.core_pcb.screws_distance_y
        pcp_support_z_over = usb_switch_box_cores.core_pcb.pcp_support_z_over

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
        support = SupportY(size_y=self.size_y, size_z=self.size_z)

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

        if True:
            pcb_support_x = SupportX(
                size_x=14, size_z=pcb_offset_z + pcp_support_z_over - SMALL
            )
            box_complete += translate(
                [-52, screws_distance_y, pcb_support_x.size_z / 2]
            )(pcb_support_x.draw())

        if True:
            pcb_support_y = SupportY(
                size_y=self.size_y, size_z=pcb_offset_z + pcp_support_z_over - SMALL
            )
            for x in (pcb_offset_x - 39, pcb_offset_x + 39):
                box_complete += (
                    translate(
                        v=[
                            x,
                            0,
                            pcb_support_y.size_z / 2 - SMALL,
                        ]
                    )(pcb_support_y.draw()),
                )

        if True:
            pcb_screws_x = (
                pcb_offset_x - screws_distance_x / 2,
                pcb_offset_x + screws_distance_x / 2,
            )
            for x in pcb_screws_x:
                box_complete += (
                    translate(
                        v=[
                            x,
                            screws_distance_y,
                            -SMALL,
                        ]
                    )(cylinder(h=pcb_offset_z, r=5)),
                )

        return box_complete - usb_switch_box_cores.draw()


SEGMENTS = 100

box = UsbSwitchBoxBottom()

scad_render_to_file(
    box.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
