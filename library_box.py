from dataclasses import dataclass
from solid import *
from solid.utils import *


@dataclass
class Corner:
    hole_xy: float = 4.0
    hole_d: float = 1.5
    r: float = 2.0
    d: float = 6.0

    def draw(self):
        return difference()(
            translate(v=[-self.r, -self.r, 0])(
                offset(r=self.r)(square([self.d, self.d]))
            ),
            # Screw hole of the corner
            translate(v=[self.hole_xy, self.hole_xy, 0])(circle(r=self.hole_d / 2)),
        )


@dataclass
class Corners:
    bounding_box = None
    corner = Corner()

    def draw(self):
        # Place corner in on corner of the box
        corner = translate(
            v=[
                -self.bounding_box.size_x / 2,
                -self.bounding_box.size_y / 2,
                0,
            ]
        )(self.corner.draw())

        # Add mirrorer corner in X direction
        cornersX = corner + mirror(v=[1, 0, 0])(corner)

        # Add mirrorer corners in Y direction
        return cornersX + mirror(v=[0, 1, 0])(cornersX)


@dataclass
class BoxSkeleton:
    size_x: float = 50.0
    size_y: float = 30.0
    size_z: float = 10.0
    wall_thickness: float = 1.0
    wall_r: float = 6.0
    cavities = union()

    def draw(self):
        # Box
        # xy-Axis: center of the box
        return difference()(
            # Outer box
            linear_extrude(height=self.size_z)(
                offset(r=self.wall_r)(
                    square(
                        [
                            self.size_x - 2 * self.wall_r,
                            self.size_y - 2 * self.wall_r,
                        ],
                        center=True,
                    )
                )
            ),
            # Inner box
            # z-Axis: on inner buttom
            translate(v=[0, 0, self.wall_thickness])(
                linear_extrude(height=self.size_z + 0.01)(
                    difference()(
                        offset(r=self.wall_r - self.wall_thickness)(
                            square(
                                [
                                    self.size_x - 2 * self.wall_r,
                                    self.size_y - 2 * self.wall_r,
                                ],
                                center=True,
                            )
                        ),
                        self.cavities,
                    )
                )
            ),
        )


@dataclass
class Box:
    corner: Corner = Corner()
    boxskeleton: BoxSkeleton = BoxSkeleton()

    def draw(self):
        corners = Corners()
        corners.bounding_box = self.boxskeleton
        corners.corner = self.corner
        self.boxskeleton.cavities = corners.draw()
        return self.boxskeleton.draw()


SEGMENTS = 100

d = Box()

scad_render_to_file(d.draw(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True)
