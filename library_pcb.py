from dataclasses import dataclass
from solid import *
from solid.utils import *


@dataclass
class CoreUsbDevice:
    size_x = 15
    size_z = 7
    size_y_dummy = 35

    def draw(self):
        return translate(v=[0, self.size_y_dummy / 2, self.size_z / 2])(
            cube(size=[self.size_x, self.size_y_dummy, self.size_z], center=True)
        )


@dataclass
class CoreUsbPC:
    size_x = 13
    size_z = 12.5
    dx = 56 / 3
    thickness_dummy = 35

    def draw(self):
        pcb = union()
        for i in [-1.5, -0.5, 0.5, 1.5]:
            x = self.dx * i
            pcb += translate(v=[x, -self.thickness_dummy / 2, self.size_z / 2])(
                cube(size=[self.size_x, self.thickness_dummy, self.size_z], center=True)
            )
        return pcb


@dataclass
class CoreBcb:
    """
    X-centered to the pcb border.
    Y-centered to the usb connectors.
    The z-zero is the top of the pcb.
    """

    size_x = 89.5
    size_y = 53.5
    usb_overall_y = 66
    usb_PC_overhead_y = 4.5
    offset_y = -(usb_overall_y / 2 - usb_PC_overhead_y - size_y / 2)
    pcb_y = 53.5 / 2 + 8.5  # Distance between device usb and center pcb
    screws_distance_x = 72
    screws_distance_y = 1.25 # The y offset of the screws to the case - Needs to be calculated correctly
    screws_y = 3  # Distance between screens and center pcb
    screws_dummy_length = 5
    screws_d = 2
    soldering_thickness = 2
    pcb_thickness = 1.6

    def draw(self):
        # PCB
        pcb = union()

        pcb += cube(size=[self.size_x, self.size_y, self.pcb_thickness], center=True)

        for x in [-self.screws_distance_x / 2, self.screws_distance_x / 2]:
            pcb += translate(
                v=[x, self.screws_y, self.soldering_thickness - self.screws_dummy_length]
            )(
                # Screws
                cylinder(d=self.screws_d, h=self.screws_dummy_length, center=True)
            )
        return translate(v=[0, self.offset_y, -self.pcb_thickness / 2])(pcb)


@dataclass
class CorePcbAssembled:
    core_pcb = CoreBcb()

    def draw(self):
        return union()(self.core_pcb.draw(), CoreUsbDevice().draw(), CoreUsbPC().draw())


SEGMENTS = 48

d = CorePcbAssembled().draw()

scad_render_to_file(d, file_header=f"$fn = {SEGMENTS};", include_orig_code=True)
