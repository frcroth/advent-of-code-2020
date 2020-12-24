with open('input.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]


def get_tile(line):
    position = (0, 0)
    while line != "":
        even_line = position[1] % 2 == 0
        if line.startswith('se'):
            line = line[2:]
            if even_line:
                position = (position[0], position[1]-1)
            else:
                position = (position[0]+1, position[1]-1)
            continue
        if line.startswith('ne'):
            line = line[2:]
            if even_line:
                position = (position[0], position[1]+1)
            else:
                position = (position[0]+1, position[1]+1)
            continue
        if line.startswith('sw'):
            line = line[2:]
            if even_line:
                position = (position[0]-1, position[1]-1)
            else:
                position = (position[0], position[1]-1)
            continue
        if line.startswith('nw'):
            line = line[2:]
            if even_line:
                position = (position[0]-1, position[1]+1)
            else:
                position = (position[0], position[1]+1)
            continue
        if line.startswith('w'):
            line = line[1:]
            position = (position[0]-1, position[1])
            continue
        if line.startswith('e'):
            line = line[1:]
            position = (position[0]+1, position[1])
            continue
    return position


def get_black_tiles():
    black_tiles = set()
    for line in content:
        tile = get_tile(line)
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)
    return black_tiles


def task_1():
    return len(get_black_tiles())


def get_neighbors(tile_position):
    even_line = tile_position[1] % 2 == 0
    if even_line:
        neighbor_offsets = [(1, 0), (0, -1), (-1, -1),
                            (-1, 0), (-1, 1), (0, 1)]
    else:
        neighbor_offsets = [(1, 0), (1, -1), (0, -1), (-1, 0), (0, 1), (1, 1)]
    neighbors = []
    for n in neighbor_offsets:
        neighbors.append((tile_position[0]+n[0], tile_position[1]+n[1]))
    return neighbors

def get_interesting_tiles(tile_dict):
    interesting = set()
    for tile in tile_dict.keys():
        interesting.update(get_neighbors(tile))
        interesting.add(tile)
    return interesting

def get_next_status_of_tile(tile, tile_dict):
    neighbors = get_neighbors(tile)
    black_count = 0
    is_black = False
    for n in neighbors:
        if n in tile_dict and tile_dict[n]:
            black_count += 1
    if tile in tile_dict and tile_dict[tile]:
        is_black = True
    if is_black and (black_count == 0 or black_count > 2):
        return False
    elif is_black:
        return True
    if black_count == 2:
        return True
    return False

def get_black_tile_count(tile_dict):
    count = 0
    for _,v in tile_dict.items():
        if v:
            count += 1
    return count

def flip_tiles(iterations = 100):
    tiles = dict()  # True = Black
    initial_black_tiles=list(get_black_tiles())
    for tile in initial_black_tiles:
        tiles[tile] = True
    for i in range(iterations+1):
        # print("Day " + str(i) + ": " + str(get_black_tile_count(tiles)))
        new_tile_dict = tiles.copy()
        interesting_tiles = list(get_interesting_tiles(tiles))
        for tile in interesting_tiles:
            status = get_next_status_of_tile(tile, tiles)
            if tile in new_tile_dict or status:
                new_tile_dict[tile] = status
        tiles = new_tile_dict
    return tiles

# Task 1
print(task_1())

# Task 2
flip_tiles()
