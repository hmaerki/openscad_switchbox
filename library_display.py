from dataclasses import dataclass
from solid import *
from solid.utils import *


@dataclass
class CoreDisplay:
    glass_thickness = 3
    glass_width = 44
    glass_height = 18
    glass_r = 3

    def draw(self):
        display = union()
        # Display
        display += rotate([90, 0, 0])(
            linear_extrude(height=self.glass_thickness)(
                offset(r=self.glass_r)(
                    square(
                        [
                            self.glass_width - 2 * self.glass_r,
                            self.glass_height - 2 * self.glass_r,
                        ],
                        center=True,
                    )
                )
            )
        )
        pcb_thickness = 2
        pcb_width = 52.5
        pcb_height = 25
        # PCB
        display += translate([-pcb_width / 2, 0, -pcb_height / 2])(
            cube([pcb_width, pcb_thickness, pcb_height])
        )
        pi_thickness = 15
        pi_width = 52
        pi_height = 21
        # Raspberry Pi Board
        display += translate([-pi_width / 2, pcb_thickness, -pi_height / 2])(
            cube([pi_width, pi_thickness, pi_height])
        )
        # Space required by Micro USB connector
        usb_center_y = 15
        usb_width = 14
        usb_thickness = 10
        usb_r = 3
        usb_dummy_length = 20
        display += translate([pi_width / 2, usb_center_y, 0])(
            rotate([0, 90, 0])(
                linear_extrude(height=usb_dummy_length)(
                    offset(r=self.glass_r)(
                        square(
                            [usb_width - 2 * usb_r, usb_thickness - 2 * usb_r],
                            center=True,
                        )
                    )
                )
            )
        )
        return display


SEGMENTS = 100

core_display = CoreDisplay()

scad_render_to_file(
    core_display.draw(), file_header=f"$fn = (SEGMENTS);", include_orig_code=True
)
