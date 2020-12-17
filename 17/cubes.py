with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]


def read_input(dim4=False):
    active_cubes = []

    for y, line in enumerate(content):
        for x, char in enumerate(line):
            if char == '#':
                if dim4:
                    active_cubes.append((x, y, 0, 0))
                else:
                    active_cubes.append((x, y, 0))
    return active_cubes


def get_neighbors(cube):
    x0, y0, z0 = cube
    neighbors = []
    for x in range(x0-1, x0+2):
        for y in range(y0-1, y0+2):
            for z in range(z0-1, z0+2):
                neighbors.append((x, y, z))
    neighbors.remove(cube)
    return neighbors


def get_neighbors_4(cube):
    x0, y0, z0, w0 = cube
    neighbors = []
    for x in range(x0-1, x0+2):
        for y in range(y0-1, y0+2):
            for z in range(z0-1, z0+2):
                for w in range(w0-1, w0+2):
                    neighbors.append((x, y, z, w))
    neighbors.remove(cube)
    return neighbors


def perform_iteration(active_cubes, dim4=False):
    interesting_cubes = []
    active_cube_dict = dict()
    active_cubes_result = []
    for cube in active_cubes:
        neighbors = get_neighbors_4(cube) if dim4 else get_neighbors(cube)
        interesting_cubes.extend(neighbors)
        active_cube_dict[cube] = True
    interesting_cubes = list(set(interesting_cubes))
    for cube in interesting_cubes:
        neighbors = get_neighbors_4(cube) if dim4 else get_neighbors(cube)
        active_neighbors = 0
        for neigh in neighbors:
            if neigh in active_cube_dict:
                active_neighbors += 1
        if cube in active_cube_dict and 2 <= active_neighbors <= 3:
            # Cube remains active
            active_cubes_result.append(cube)
        if cube not in active_cube_dict and active_neighbors == 3:
            active_cubes_result.append(cube)
    return active_cubes_result


def perform_iterations(number, initial_active, dim4=False):
    active = initial_active
    for i in range(number):
        active = perform_iteration(active, dim4)
    return active


def sum_of_actives(active_cubes):
    return len(active_cubes)


def task_1():
    return sum_of_actives(perform_iterations(6, read_input()))


def task_2():
    return sum_of_actives(perform_iterations(6, read_input(True), True))


print(task_1())

print(task_2())
