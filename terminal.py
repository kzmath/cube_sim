###############################
####  Rendering Code ##########
###############################



block = "\u2588"

colors = {
    "W": 255,  # Off-white/light gray (instead of 15)
    "Y": 220,  # Muted yellow (instead of 226)
    "R": 124,  # Muted red (instead of 196)
    "O": 172,  # Muted orange (instead of 208)
    "B": 27,  # Muted blue (instead of 21)
    "G": 34,  # Muted green (instead of 46)
    "_": 0,
}

class Face:
    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        result = ""
        for row in self.rows:
            result += f"{row}" + "\n"
        return result


def print_block(color, end=""):
    print(f"\033[38;5;{color}m{block}{block}\033[0m", end=end)


def print_faces(faces):
    """faces are a list of Face objects or None"""
    spacing = " " * 2
    N = len(faces)

    # First line
    for n in range(N):
        if faces[n] == None:
            print(" " * 10, end="")
        else:
            print("┌──┬──┬──┐", end="")
        print(spacing, end="")
    print()

    # middle lines
    for i in range(3):
        # print a line of blocks
        for n in range(N):
            if faces[n] == None:
                print(" " * 10, end="")
            else:
                print("│", end="")
                for j in range(3):
                    if faces[n] == None:
                        print(" " * 10, end="")
                    else:
                        print_block(colors[faces[n].rows[i][j]], end="│")
            print(spacing, end="")
        print()
        # print divider lines
        if i < 2:
            for n in range(N):
                if faces[n] == None:
                    print(" " * 10, end="")
                else:
                    print("├──┼──┼──┤", end="")
                print(spacing, end="")
            print()

    # Bottom line
    for n in range(N):
        if faces[n] == None:
            print(" " * 10, end="")
        else:
            print("└──┴──┴──┘", end="")
        print(spacing, end="")
    print()


def print_faces_merged(faces, spaces=0):
    spacing = " " * spaces
    N = len(faces)

    for i in range(3):
        # print a line of blocks
        for n in range(N):
            if faces[n] == None:
                print(" " * 6, end="")
            else:
                for j in range(3):
                    print_block(colors[faces[n].rows[i][j]])
            print(spacing, end="")
        print()


def get_face(cube, direction):
    """Get the face in that direction"""
    rows = [[], [], []]
    if direction == "F":
        # reversed z, x, y = 0
        for z in range(3):
            for x in range(3):
                rows[z].append(cube.get_color((x, 0, 2 - z), direction))
    if direction == "B":
        # reversed z, reversed x, y = 2
        for z in range(3):
            for x in range(3):
                rows[z].append(cube.get_color((2 - x, 2, 2 - z), direction))
    if direction == "L":
        # reversed z, reversed y, x = 0
        for z in range(3):
            for y in range(3):
                rows[z].append(cube.get_color((0, 2 - y, 2 - z), direction))
    if direction == "R":
        # reversed z, y, x = 2
        for z in range(3):
            for y in range(3):
                rows[z].append(cube.get_color((2, y, 2 - z), direction))
    if direction == "D":
        # y, x, z = 0
        for y in range(3):
            for x in range(3):
                rows[y].append(cube.get_color((x, y, 0), direction))
    if direction == "U":
        # reversed y, x, z = 2
        for y in range(3):
            for x in range(3):
                rows[y].append(cube.get_color((x, 2 - y, 2), direction))
    return Face(rows)


def print_net(cube):
    print_faces_merged([None, get_face(cube, "U")])
    print_faces_merged(
        [
            get_face(cube, "L"),
            get_face(cube, "F"),
            get_face(cube, "R"),
            get_face(cube, "B"),
        ]
    )
    print_faces_merged([None, get_face(cube, "D")])


def cube_test(test_cube):
    ## Test Move
    print("Front")
    test_cube.move("F")
    print_net(test_cube)
    test_cube.move("F'")
    print_net(test_cube)
    print("Back")
    test_cube.move("B")
    print_net(test_cube)
    test_cube.move("B'")
    print_net(test_cube)
    print("Right")
    test_cube.move("R")
    print_net(test_cube)
    test_cube.move("R'")
    print_net(test_cube)
    test_cube.move("R3")
    print_net(test_cube)
    test_cube.move("R3'")
    print_net(test_cube)
    print("Left")
    test_cube.move("L")
    print_net(test_cube)
    test_cube.move("L'")
    print_net(test_cube)
    print("Up")
    test_cube.move("U")
    print_net(test_cube)
    test_cube.move("U'")
    print_net(test_cube)
    print("Down")
    test_cube.move("D")
    print_net(test_cube)
    test_cube.move("D'")
    print_net(test_cube)
