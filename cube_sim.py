class Orientation:
    def __init__(self, x="R", y="B", z="U"):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"x={self.x}, y={self.y}, z={self.z}"


class Transformation:
    def __init__(self, image):
        self.image = image
        self.source = ["L", "R", "F", "B", "D", "U"]
        self.map = {}
        for i in range(len(self.source)):
            self.map[self.source[i]] = image[i]

    def transform(self, direction):
        return self.map[direction]

    def transform_orientation(self, orientation):
        return Orientation(
            x=self.transform(orientation.x),
            y=self.transform(orientation.y),
            z=self.transform(orientation.z),
        )


TR_opposite = Transformation(["R", "L", "B", "F", "U", "D"])
TR_rx = Transformation(["L", "R", "U", "D", "F", "B"])
TR_rxp = Transformation(["L", "R", "D", "U", "B", "F"])
TR_rz = Transformation(["B", "F", "L", "R", "D", "U"])
TR_rzp = Transformation(["F", "B", "R", "L", "D", "U"])
TR_ry = Transformation(["D", "U", "F", "B", "R", "L"])
TR_ryp = Transformation(["U", "D", "F", "B", "L", "R"])


def right_turn(x, y):
    return y, 2 - x


def left_turn(x, y):
    return 2 - y, x


class Rotation:
    def __init__(self, axis, clockwise, layers):
        """axis should be 'x', 'y', 'z',
        clockwise should be True, False
        layers is a sublist of [0, 1, 2]"""
        self.axis = axis
        self.layers = layers
        self.clockwise = clockwise
        if self.axis == "x":
            self.tr = TR_rx if clockwise else TR_rxp
            self.fix = 0
        if self.axis == "y":
            self.tr = TR_ry if clockwise else TR_ryp
            self.fix = 1
        if self.axis == "z":
            self.tr = TR_rz if clockwise else TR_rzp
            self.fix = 2

    def rotate(self, position, orientation):
        pos = list(position)
        ri = [(self.fix + 1) % 3, (self.fix + 2) % 3]
        new_pos = list(pos)
        if self.clockwise:
            new_pos[ri[0]], new_pos[ri[1]] = right_turn(new_pos[ri[0]], new_pos[ri[1]])
        else:
            new_pos[ri[0]], new_pos[ri[1]] = left_turn(new_pos[ri[0]], new_pos[ri[1]])
        new_orientation = self.tr.transform_orientation(orientation)
        return tuple(new_pos), new_orientation

    def move(self, position, orientation):
        pos = list(position)
        if pos[self.fix] in self.layers:
            return self.rotate(position, orientation)
        else:
            return position, orientation


class BlockColor:
    def __init__(self, position):
        self.L = "O"
        self.R = "R"
        self.F = "B"
        self.B = "G"
        self.D = "W"
        self.U = "Y"
        x, y, z = position
        if x != 0:
            self.L = "_"
        if x != 2:
            self.R = "_"
        if y != 0:
            self.F = "_"
        if y != 2:
            self.B = "_"
        if z != 0:
            self.D = "_"
        if z != 2:
            self.U = "_"

    def __str__(self):
        return f"L={self.L}, R={self.R}, F={self.F}, B={self.B}, D={self.D}, U={self.U}"


class BlockState:
    def __init__(self, position, orientation):
        # position is (i, j, k) with i, j, k in range(3)
        # Orientation is an Orientation object
        # by default x = "R", y = "B", z = "U", i.e.
        # front, back, up for x, y, z axes
        self.position = position
        self.orientation = orientation

    def __str__(self):
        return f"position: {self.position}, orientation: {self.orientation}"


class Cube:
    def __init__(self):
        self.state = {}
        self.block_colors = {}
        # Initial state
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # self.state[(i, j, k)] records current position
                    # and orienation of the block (i, j, k)
                    self.state[(i, j, k)] = BlockState((i, j, k), Orientation())

        # Initial colors
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.block_colors[(i, j, k)] = BlockColor((i, j, k))

        # Moves
        self.moves = {}

        self.moves["R"] = Rotation("x", True, [2])
        self.moves["R'"] = Rotation("x", False, [2])
        self.moves["L"] = Rotation("x", False, [0])
        self.moves["L'"] = Rotation("x", True, [0])
        self.moves["U"] = Rotation("z", True, [2])
        self.moves["U'"] = Rotation("z", False, [2])
        self.moves["D"] = Rotation("z", False, [0])
        self.moves["D'"] = Rotation("z", True, [0])
        self.moves["B"] = Rotation("y", True, [2])
        self.moves["B'"] = Rotation("y", False, [2])
        self.moves["F"] = Rotation("y", False, [0])
        self.moves["F'"] = Rotation("y", True, [0])

        self.moves["M"] = Rotation("x", True, [1])

        self.moves["R3"] = Rotation("x", True, [0, 1, 2])
        self.moves["R3'"] = Rotation("x", False, [0, 1, 2])

    def move(self, name):
        mv = self.moves[name]
        for pos in self.state:
            self.state[pos] = BlockState(
                *mv.move(self.state[pos].position, self.state[pos].orientation)
            )

    def reset(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # self.state[(i, j, k)] records current position
                    # and orienation of the block (i, j, k)
                    self.state[(i, j, k)] = BlockState((i, j, k), Orientation())


    ## Rendering code
    def get_color(self, target_position, direction):
        """Get color for the cube at given position facing direction"""
        position = None
        for pos in self.state:
            if self.state[pos].position == target_position:
                position = pos
                break
        orientation = self.state[position].orientation
        block_color = self.block_colors[position]
        if direction in [orientation.x, TR_opposite.transform(orientation.x)]:
            return block_color.R if direction == orientation.x else block_color.L
        if direction in [orientation.y, TR_opposite.transform(orientation.y)]:
            return block_color.B if direction == orientation.y else block_color.F
        if direction in [orientation.z, TR_opposite.transform(orientation.z)]:
            return block_color.U if direction == orientation.z else block_color.D

    def __str__(self):
        result = ""
        for pos in self.state:
            result += (
                f"{pos}: {self.state[pos].position}, {self.state[pos].orientation}"
                + "\n"
            )
        return result


def terminal_test():
    from terminal import cube_test

    test_cube = Cube()
    cube_test(test_cube)


##############################
##### PyGame Renderer ########
##############################

import pygame
import math
from pygame.math import Vector2
import pygame.draw as draw
import pygame.gfxdraw as gfx


colors = {
    "W": (240, 240, 245),
    "Y": (255, 200, 46),
    "R": (220, 50, 50),
    "O": (255, 120, 30),
    "B": (30, 100, 200),
    "G": (40, 180, 99),
}


x_axis = Vector2.from_polar((1, 30))
y_axis = Vector2.from_polar((1, -30))
z_axis = Vector2.from_polar((1, -90))


def make_rombus(corner, side, va, vb):
    """Returns the vertices of a parallelogram"""
    return (
        corner,
        corner + va * side,
        corner + va * side + vb * side,
        corner + vb * side,
    )


def polygon(surface, points, color, line_color=(0, 0, 0)):
    gfx.filled_polygon(surface, points, color)
    gfx.aapolygon(surface, points, line_color)



def get_face_color(cube, face, i, j):
    if face == "F":
        return cube.get_color((i, 0, j), face)
    if face == "B":
        return cube.get_color((i, 2, j), face)
    if face == "D":
        return cube.get_color((i, j, 0), face)
    if face == "U":
        return cube.get_color((i, j, 2), face)
    if face == "R":
        return cube.get_color((2, i, j), face)
    if face == "L":
        return cube.get_color((0, i, j), face)

def draw_face_impl(surface, cube, face, corner, va, vb, side):
    for i in range(3):  # x offset
        for j in range(3):  # y offset
            polygon(
                surface,
                make_rombus(
                    corner + i * va * side/3 + j * vb * side/3, side/3, va, vb
                ),
                colors[get_face_color(cube, face, i, j)]),


def draw_face(surface, cube, face, base, side):
    """Draw the face of a cube with side length <side>.
    The <base> point of the face is the center vertex"""
    if face == "F":
        corner = base - side * z_axis - side * x_axis
        draw_face_impl(surface, cube, face, corner, x_axis, z_axis, side)
    if face == "R":
        corner = base - side * z_axis
        draw_face_impl(surface, cube, face, corner, y_axis, z_axis, side)
    if face == "U":
        corner = base - side * x_axis
        draw_face_impl(surface, cube, face, corner, x_axis, y_axis, side)
    if face == "B":
        corner = base
        draw_face_impl(surface, cube, face, corner, x_axis, z_axis, side)
    if face == "L":
        corner = base - side * y_axis
        draw_face_impl(surface, cube, face, corner, y_axis, z_axis, side)
    if face == "D":
        corner = base - side * z_axis - side * x_axis
        draw_face_impl(surface, cube, face, corner, x_axis, y_axis, side)

def draw_cube(surface, cube, center, side):
    origin = Vector2(center)
    draw_face(surface, cube, "F", origin, side)
    draw_face(surface, cube, "R", origin, side)
    draw_face(surface, cube, "U", origin, side)

    draw_face(surface, cube, "B", origin + 1.2*side*y_axis, side)
    draw_face(surface, cube, "L", origin - 1.2*side*x_axis, side)
    draw_face(surface, cube, "D", origin - 1.2*side*z_axis, side)

def main():
    pygame.init()
    width = 1280
    height = 720
    pygame.display.set_caption("Rubik's cube simulator")
    screen = pygame.display.set_mode((width, height), pygame.SCALED)
    clock = pygame.time.Clock()
    running = True
    cube = Cube()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                pressed = pygame.key.get_pressed()
                shift_pressed = pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]
                if event.key == pygame.K_r and (not shift_pressed):
                    cube.move("R")
                if event.key == pygame.K_r and shift_pressed:
                    cube.move("R'")
                if event.key == pygame.K_l and (not shift_pressed):
                    cube.move("L")
                if event.key == pygame.K_l and shift_pressed:
                    cube.move("L'")
                if event.key == pygame.K_f and (not shift_pressed):
                    cube.move("F")
                if event.key == pygame.K_f and shift_pressed:
                    cube.move("F'")
                if event.key == pygame.K_b and (not shift_pressed):
                    cube.move("B")
                if event.key == pygame.K_b and shift_pressed:
                    cube.move("B'")
                if event.key == pygame.K_d and (not shift_pressed):
                    cube.move("D")
                if event.key == pygame.K_d and shift_pressed:
                    cube.move("D'")
                if event.key == pygame.K_u and (not shift_pressed):
                    cube.move("U")
                if event.key == pygame.K_u and shift_pressed:
                    cube.move("U'")
                if event.key == pygame.K_m:
                    cube.move("M")

                if event.key == pygame.K_SPACE:
                    cube.reset()


        screen.fill("black")

        draw_cube(screen, cube, (width / 2, height / 2), 150)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
