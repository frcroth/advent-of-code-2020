initial_label = [5, 8, 3, 9, 7, 6, 2, 4, 1]
#initial_label = [3, 8, 9, 1, 2, 5, 4, 6, 7]


def play_round(cups, current_cup_index):
    current_cup = cups[current_cup_index]
    pick_up = []

    if current_cup_index + 4 > len(cups) - 1:
        if current_cup_index+1 <= len(cups) - 1:
            pick_up_back = current_cup_index + 1
        else:
            pick_up_back = len(cups)
        pick_up_front = 3 - (len(cups) - pick_up_back)
        pick_up = cups[pick_up_back:] + cups[:pick_up_front]
        cups = cups[pick_up_front:pick_up_back]
    else:
        pick_up = cups[current_cup_index+1:current_cup_index+4]
        cups = cups[:current_cup_index+1] + cups[current_cup_index+4:]

    # get destination cup
    lowest_value = min(cups)
    destination_value = current_cup - 1
    while not destination_value in cups:
        destination_value -= 1
        if destination_value < lowest_value:
            destination_value = int(max(cups))
    destination_index = cups.index(destination_value)

    # insert pick up
    cups = cups[:destination_index+1] + pick_up + cups[destination_index+1:]
    # new current cup
    current_cup_index = (cups.index(current_cup) + 1) % len(cups)

    return cups, current_cup_index


def generate_output(cups):
    one = cups.index(1)
    return cups[one+1:] + cups[:one]


def play_game(game_count):
    cups, current = initial_label, 0
    for _ in range(game_count):
        cups, current = play_round(cups, current)
    return(generate_output(cups))


def init_crab_cubs(initial_cups):
    cups = dict()
    for i, cup in enumerate(initial_cups):
        if i != len(initial_cups)-1:
            cups[cup] = initial_cups[i+1]
    cups[initial_cups[len(initial_cups)-1]] = 10
    for i in range(10, int(1e6) + 1):
        if i != int(1e6):
            cups[i] = i+1
    cups[int(1e6)] = initial_cups[0]
    return cups


def play_crab_game(game_count, cups, current_cup):
    for _ in range(game_count-1):
        pick_up1 = cups[current_cup]
        pick_up2 = cups[pick_up1]
        pick_up3 = cups[pick_up2]

        after_pick_up = cups[pick_up3]
        cups[current_cup] = after_pick_up

        # find destination
        destination_value = current_cup-1
        while True:
            if destination_value in cups:
                if destination_value != pick_up1 and destination_value != pick_up2 and destination_value != pick_up3:
                    break
            destination_value -= 1
            if destination_value < 1:
                destination_value = int(1e6)

        # insert pick up
        after_dest = cups[destination_value]
        cups[destination_value] = pick_up1
        cups[pick_up3] = after_dest

        current_cup = cups[current_cup]

    return cups


def play_crab_edition():
    game_count = int(1e7)
    cups = init_crab_cubs(initial_label)
    cups = play_crab_game(game_count, cups, initial_label[0])
    after_one = cups[1]
    after_after_one = cups[after_one]
    return after_one * after_after_one

# Task 1
print(play_game(100))

# Task 2
print(play_crab_edition())
