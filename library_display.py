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
    glass_width = 48
    glass_height = 20
    glass_r = 3
    is_top: bool

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
        pcb_width = 53
        pcb_height = 25
        display += translate([-pcb_width / 2, self.glass_thickness, -pcb_height / 2])(
            cube([pcb_width, pcb_thickness, pcb_height])
        )

        # Raspberry Pi Board
        pi_thickness = 14.3
        pi_width = 52
        pi_height = 21
        display += translate(
            [-pi_width / 2, self.glass_thickness + pcb_thickness, -pi_height / 2]
        )(cube([pi_width, pi_thickness, pi_height]))

        # USB
        usb_center_y = 18
        display += translate([pi_width / 2, usb_center_y, 0])(CoreDisplayUsb().draw())

        if not self.is_top:
            # Reset Button
            for x in (13, -9):
                for z in (-3, -2, -1, 0, 1, 2):
                    display += translate(v=[x, 25, z])(debug(rotate([90, 0, 0])(cylinder(d=5, h=10))))

        return display


SEGMENTS = 100

core_display = CoreDisplay(is_top=False)

scad_render_to_file(
    core_display.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
)
