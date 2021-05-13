from dataclasses import dataclass
from solid import *
from solid.utils import *


@dataclass
class CoreDisplayUsb:
    # Space required by Micro USB connector
    usb_width = 14
    usb_thickness = 10
    usb_r = 3
    usb_dummy_length = 20

    def draw(self):
        return rotate([0, 90, 0])(
            linear_extrude(height=self.usb_dummy_length)(
                offset(r=self.usb_r)(
                    square(
                        [
                            self.usb_width - 2 * self.usb_r,
                            self.usb_thickness - 2 * self.usb_r,
                        ],
                        center=True,
                    )
                )
            )
        )


@dataclass
class CoreDisplay:
    glass_thickness = 3
    glass_width = 44
    glass_height = 18
    glass_r = 3

    def draw(self):
        display = union()
        # Display glass
        display += translate(v=[0, self.glass_thickness, 0])(
            rotate([90, 0, 0])(
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
        )

        # PCB
        pcb_thickness = 2
        pcb_width = 52.5
        pcb_height = 25
        display += translate([-pcb_width / 2, self.glass_thickness, -pcb_height / 2])(
            cube([pcb_width, pcb_thickness, pcb_height])
        )

        # Raspberry Pi Board
        pi_thickness = 15
        pi_width = 52
        pi_height = 21
        display += translate([-pi_width / 2,self.glass_thickness+ pcb_thickness, -pi_height / 2])(
            cube([pi_width, pi_thickness, pi_height])
        )

        # USB
        usb_center_y = 15
        display += translate([pi_width / 2, usb_center_y, 0])(
            CoreDisplayUsb().draw()
        )
        return display


SEGMENTS = 100

core_display = CoreDisplay()

scad_render_to_file(
    core_display.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
