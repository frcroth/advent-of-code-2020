
def read_tiles():

    with open('input.txt') as f:
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


def build_image():
    transform_dict = build_transformation_dict(read_tiles())
    solve()
    image = []
    for tile_row in solution:
        tiles = []
        for tile_id, transformation_id in tile_row:
            tile = transform_dict[tile_id][transformation_id]
            tiles.append([line[1:-1] for line in tile[1:-1]])
        for y in range(len(tiles[0][0])):
            current_line = []
            for i in range(len(tiles)):
                current_line.extend(tiles[i][x][y]
                                    for x in range(len(tiles[i])))
            image.append(current_line)
    return image


monster = [(18, 0), (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1),
           (18, 1), (19, 1), (1, 2), (4, 2), (7, 2), (10, 2), (13, 2), (16, 2)]


def is_sea_monster(image, x, y):
    dimension = len(image)
    extent_x = 20
    extent_y = 3
    if x + extent_x - 1 > dimension or y + extent_y - 1 > dimension:
        return False
    for x_pos, y_pos in monster:
        if image[y_pos+y][x_pos+x] != '#':
            return False
    return True


def get_sea_monster_position(image, x, y):
    positions_in_image = []
    for x_pos, y_pos in monster:
        positions_in_image.append((x_pos+x, y_pos+y))
    return positions_in_image


def get_sea_monster_transformation(image):
    transformations = get_transformations(image)
    for transformation in transformations:
        for y in range(len(image)):
            for x in range(len(image)):
                if is_sea_monster(transformation, x, y):
                    return transformation


def count_non_sea_monsters(image):
    sea_monster_tiles = set()
    for y in range(len(image)):
        for x in range(len(image)):
            if is_sea_monster(image, x, y):
                sea_monster_tiles.update(
                    set(get_sea_monster_position(image, x, y)))
    count = 0
    for y in range(len(image)):
        for x in range(len(image)):
            if image[y][x] == '#' and (x, y) not in sea_monster_tiles:
                count += 1

    return count


def task_2():
    image = build_image()
    sea_monster_transformation = get_sea_monster_transformation(image)
    return count_non_sea_monsters(sea_monster_transformation)


def task_1():
    solve()
    return int(solution[0][0][0]) * int(solution[0][-1][0]) * int(solution[-1][0][0]) * int(solution[-1][-1][0])


print(task_1())

print(task_2())
