from dataclasses import dataclass
from solid import *
from solid.utils import *


@dataclass
class CoreUsbDevice:
    width = 15
    height = 7
    thickness_dummy = 100

    def draw(self):
        return translate(v=[-self.thickness_dummy, -self.width / 2, 0])(
            cube(size=[self.thickness_dummy, self.width, self.height], center=False)
        )


@dataclass
class CoreUsbPcb:
    width = 12
    height = 12.5
    dy = 56 / 3
    thickness_dummy = 100

    def draw(self):
        pcb = union()
        for i in [-1.5, -0.5, 0.5, 1.5]:
            y = self.dy * i - self.width / 2
            pcb += translate(v=[0, y, 0])(
                cube(size=[self.thickness_dummy, self.width, self.height], center=False)
            )
        return pcb


@dataclass
class CoreBcb:
    pcb_width = 89.5
    pcb_depth = 53.5
    pcb_x = 4
    screws_distance_y = 72
    screws_x = 34
    screws_length = 6
    soldering_thickness = 2
    pcb_thickness = 1.6

    def draw(self):
        # PCB
        pcb = union()
        pcb += cube(
            size=[self.pcb_depth, self.pcb_width, self.pcb_thickness], center=False
        )
        for y in [-self.screws_distance_y / 2, self.screws_distance_y / 2]:
            pcb += translate(
                v=[self.screws_x, y, self.soldering_thickness - self.screws_length]
            )(
                # Screws
                cylinder(d=2, h=self.screws_length, center=True)
            )
        return pcb


SEGMENTS = 48

d = union()(CoreBcb().draw(), CoreUsbDevice().draw(), CoreUsbPcb().draw())

scad_render_to_file(d, file_header=f"$fn = {SEGMENTS};", include_orig_code=True)
