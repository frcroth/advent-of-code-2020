
def read_tiles():

    with open('example1.txt') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    tiles = dict()
    current_tile = []
    current_tile_id = ''
    for line in content:
        if 'Tile' in line:
            current_tile_id = line.split(' ')[1].split(':')[0]
        elif line == '':
            tiles[current_tile_id] = current_tile
            current_tile = []
            continue
        else:
            current_tile.append(list(line))
    tiles[current_tile_id] = current_tile
    return tiles


def get_borders(tile):
    # up, right, down, left
    return [list(tile[0]), [line[-1] for line in tile], list(tile[-1]), [line[0] for line in tile]]


def get_flips(tile):
    return [tile, tile[::-1],  [line[::-1] for line in tile], [line[::-1] for line in tile][::-1]]


def rotate_tile(tile):
    return list(zip(*tile.copy()[::-1]))


def get_rotations(tile):
    result = [tile]
    for _ in range(3):
        rotated_tile = rotate_tile(tile)
        result.append(rotated_tile)
    return result


def get_transformations(tile):
    flips = get_flips(tile)
    result = []
    for tile in flips:
        rotations = get_rotations(tile)
        for rotation in rotations:
            if rotation not in result:
                result.append(rotation)
    return result


def build_transformation_dict(tiles):
    transform_dict = dict()
    for tile_id, tile in tiles.items():
        transform_dict[tile_id] = get_transformations(tile)
    return transform_dict


def build_transformation_border_dict(transform_dict):
    transformation_border_dict = dict()
    for tile_id, transformations in transform_dict.items():
        transformation_border_dict[tile_id] = []
        for transformation in transformations:
            transformation_border_dict[tile_id].append(
                get_borders(transformation))
    return transformation_border_dict


def get_dimension(tiles):
    return int(len(tiles) ** 0.5)


def get_empty_tile_array(tiles):
    return [[None] * get_dimension(tiles) for _ in range(get_dimension(tiles))]


def build_tile_array(tile_array, dimension, transform_dict, transformation_border_dict, x=0, y=0, placed=set()):
    if y == dimension:
        # Done
        return tile_array
    nextX = x+1
    nextY = y
    if nextX > dimension-1:
        nextY = y+1
        nextX = 0
    for tile_id, transformations in transform_dict.items():
        if tile_id in placed:
            continue
        placed.add(tile_id)
        for i, _ in enumerate(transformations):
            up, _, _, left = transformation_border_dict[tile_id][i]
            if x > 0:
                # We need to check if left fits
                neighbor_tile_id, neighbor_transformation_id = tile_array[x-1][y]
                _, n_right, _, _ = transformation_border_dict[neighbor_tile_id][neighbor_transformation_id]
                if n_right != left:
                    continue
            if y > 0:
                # We need to check if top fits
                neighbor_tile_id, neighbor_transformation_id = tile_array[x][y-1]
                _, _, n_down, _ = transformation_border_dict[neighbor_tile_id][neighbor_transformation_id]
                if n_down != up:
                    continue
            tile_array[x][y] = (tile_id, i)
            result = build_tile_array(
                tile_array, dimension, transform_dict, transformation_border_dict, nextX, nextY, placed)
            if result is not None:
                # returning from success
                return result
        placed.remove(tile_id)
    tile_array[x][y] = None
    return None


def print_tile(tile):
    for line in tile:
        print(''.join(map(str, line)))
    print("\n")


def print_tile_id_array(tile_array):
    print(str(tile_array[0][0]) + "|" +
          str(tile_array[1][0]) + "|" + str(tile_array[2][0]))
    print(str(tile_array[0][1]) + "|" +
          str(tile_array[1][1]) + "|" + str(tile_array[2][1]))
    print(str(tile_array[0][2]) + "|" +
          str(tile_array[1][2]) + "|" + str(tile_array[2][2]))


solution = None


def solve():
    global solution
    tiles = read_tiles()
    transform_dict = build_transformation_dict(tiles)
    transformation_border_dict = build_transformation_border_dict(
        transform_dict)
    dimension = get_dimension(tiles)
    new_solution = build_tile_array(get_empty_tile_array(
        tiles), dimension, transform_dict, transformation_border_dict)
    if new_solution is not None:
        solution = new_solution


def get_tile_without_border(tile):
    tile.pop(0)
    tile.pop(len(tile)-1)
    new_tile = []
    for line in tile:
        new_tile.append(line[1:-1])
    return new_tile


def build_image():
    tiles = read_tiles()
    transform_dict = build_transformation_dict(tiles)
    solve()
    image = []
    for tile_row in solution:
        tiles = []
        for tile_id, transformation_id in tile_row:
            tiles.append(get_tile_without_border(
                transform_dict[tile_id][transformation_id]))
        print(tiles[0])
        for i in range(len(tiles[0])):
            current_line = []
            for tile in tiles:
                current_line.extend(tile[i])
            image.append(current_line)
    return image


def task_1():
    solve()
    return int(solution[0][0][0]) * int(solution[0][-1][0]) * int(solution[-1][0][0]) * int(solution[-1][-1][0])


print(task_1())

print(build_image())
