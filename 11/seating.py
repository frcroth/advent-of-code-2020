from collections import Counter

with open('input.txt') as f:
    content = f.readlines()

matrix = [x.strip() for x in content]
init_matrix = matrix


def save_array_access(seat_x, seat_y):
    if 0 <= seat_y < len(matrix) and 0 <= seat_x < len(matrix[0]):
        return matrix[seat_y][seat_x]


def get_adjacent_seats(seat_x, seat_y):
    adjacent = []
    adjacent.append(save_array_access(seat_x-1, seat_y))
    adjacent.append(save_array_access(seat_x+1, seat_y))
    adjacent.append(save_array_access(seat_x, seat_y+1))
    adjacent.append(save_array_access(seat_x, seat_y-1))
    adjacent.append(save_array_access(seat_x-1, seat_y+1))
    adjacent.append(save_array_access(seat_x-1, seat_y-1))
    adjacent.append(save_array_access(seat_x+1, seat_y+1))
    adjacent.append(save_array_access(seat_x+1, seat_y-1))

    return list(filter(None, adjacent))


def next_state_1(seat_x, seat_y):
    seat = matrix[seat_y][seat_x]
    if seat == '.':
        return '.'
    adjacent = get_adjacent_seats(seat_x,  seat_y)
    occupied = Counter(adjacent)['#']
    if seat == 'L' and occupied == 0:
        return '#'
    if seat == '#' and occupied >= 4:
        return 'L'
    return seat


def see_seats(seat_x, seat_y, diff_x, diff_y):
    seat = save_array_access(seat_x, seat_y)
    if not seat:
        return '.'
    if seat == 'L':
        return 'L'
    if seat == '#':
        return '#'
    else:
        return see_seats(seat_x + diff_x, seat_y + diff_y, diff_x, diff_y)


def get_seats_seen(seat_x, seat_y):
    seen = []
    # horizontal
    seen.append(see_seats(seat_x+1, seat_y, 1, 0))
    seen.append(see_seats(seat_x-1, seat_y, -1, 0))
    # vertical
    seen.append(see_seats(seat_x, seat_y+1, 0, 1))
    seen.append(see_seats(seat_x, seat_y-1, 0, -1))
    # diagonal
    seen.append(see_seats(seat_x+1, seat_y+1, 1, 1))
    seen.append(see_seats(seat_x-1, seat_y+1, -1, 1))
    seen.append(see_seats(seat_x+1, seat_y-1, 1, -1))
    seen.append(see_seats(seat_x-1, seat_y-1, -1, -1))

    return seen


def next_state_2(seat_x, seat_y):
    seat = matrix[seat_y][seat_x]
    if seat == '.':
        return '.'
    seen = get_seats_seen(seat_x, seat_y)
    occupied = Counter(seen)['#']
    if seat == 'L' and occupied == 0:
        return '#'
    if seat == '#' and occupied >= 5:
        return 'L'
    return seat


def perform_iteration(rule):
    global matrix
    new_matrix = []
    for i in range(len(matrix)):
        new_row = []
        for j in range(len(matrix[0])):
            if rule == 1:
                new_row.append(next_state_1(j, i))
            else:
                new_row.append(next_state_2(j, i))
        new_matrix.append(new_row)
    matrix = new_matrix


def count_occupied():
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '#':
                count += 1
    return count


def task_1():
    global matrix
    matrix = init_matrix
    last_count = -1

    while True:
        new_count = count_occupied()
        if last_count == new_count:
            return last_count
        last_count = new_count
        perform_iteration(1)


def task_2():
    global matrix
    matrix = init_matrix
    last_count = -1

    while True:
        new_count = count_occupied()
        if last_count == new_count:
            return last_count
        last_count = new_count
        perform_iteration(2)


print(task_1())

print(task_2())
