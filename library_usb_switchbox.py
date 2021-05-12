from dataclasses import dataclass
from solid import *
from solid.utils import *

import library_box
import library_pcb
import library_display

@dataclass
class UsbSwitchBox():
    enclosureWidth = 65
    enclosureLength = 130
    enclosureHeightTray = 16
    enclosureHeightCover = 8
    hullThickness = 2
    cornerRadius = 2.5
    screwDiameter = 3

    def draw(self):
        display_y = self.hullThickness-self.enclosureLength/2
        display_z = 14
        display_support1_y = 12
        display_support2_y = 17

        corner = library_box.Corner()
        boxskeleton = library_box.BoxSkeleton(size_x=self.enclosureLength, size_y=self.enclosureWidth, size_z=self.enclosureHeightTray, wall_thickness=self.hullThickness)
        box = library_box.Box(boxskeleton=boxskeleton, corner=corner)

        # The tray of the housing:
        return translate(v=[-self.enclosureWidth / 2 -10, 0, self.enclosureHeightTray/2]) (
            difference() (
                union () (
                    # tray(self.enclosureWidth, self.enclosureLength, self.enclosureHeightTray, self.hullThickness, self.cornerRadius, self.screwDiameter),
                    box.draw(),
                    translate(v=[-self.enclosureWidth/2, display_y+display_support1_y, 0]) (
                            cube(size=[self.enclosureWidth, 2, self.enclosureHeightTray])
                    ),
                    translate(v=[-self.enclosureWidth/2, display_y+display_support2_y, 0]) (
                            cube(size=[self.enclosureWidth, 2, self.enclosureHeightTray])
                    )
                ),
                union () (
                    # Display
                    translate(v=[0, display_y, display_z]) (
                        library_display.CoreDisplay().draw()
                    ),
                    # 4 PC USB ports
                    translate(v=[0, 0, 8]) (
                        library_pcb.CoreUsbPcb().draw()
                    ),
                    # 1 Device USB port
                    translate(v=[0, 0, 9]) (
                        library_pcb.CoreUsbDevice().draw()
                    )
                )
            )
        )

SEGMENTS = 100

core_display = UsbSwitchBox()

scad_render_to_file(
    core_display.draw(), file_header=f"$fn = (SEGMENTS);", include_orig_code=True
)
