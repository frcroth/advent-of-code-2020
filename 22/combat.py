with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]
player_cards = dict()
player_cards[1] = []
player_cards[2] = []
player = 1
for line in content:
    if 'Player 1' in line:
        player = 1
        continue
    elif 'Player 2' in line:
        player = 2
        continue
    elif line != "":
        player_cards[player].append(int(line))


def play_round(player_1_cards, player_2_cards):
    player_1_card = player_1_cards.pop(0)
    player_2_card = player_2_cards.pop(0)
    winner = 1 if player_1_card > player_2_card else 2
    if winner == 1:
        player_1_cards.append(player_1_card)
        player_1_cards.append(player_2_card)
    else:
        player_2_cards.append(player_2_card)
        player_2_cards.append(player_1_card)
    return player_1_cards, player_2_cards


def get_winner(player_1_cards, player_2_cards):
    if len(player_1_cards) == 0:
        return 2
    if len(player_2_cards) == 0:
        return 1


def count_points(cards):
    cards_reversed = cards[::-1]
    points = 0
    for i, card in enumerate(cards_reversed):
        points += (i+1) * card
    return points


def play_game_1():
    player_1_cards = player_cards[1].copy()
    player_2_cards = player_cards[2].copy()
    while True:
        winner = get_winner(player_1_cards, player_2_cards)
        if winner == None:
            player_1_cards, player_2_cards = play_round(
                player_1_cards, player_2_cards)
        elif winner == 1:
            return count_points(player_1_cards)
        elif winner == 2:
            return count_points(player_2_cards)


def get_round_hash(player_1_cards, player_2_cards):
    return str(player_1_cards) + str(player_2_cards)


def play_recursive_game(player_1_cards, player_2_cards, previous_rounds=set()):
    while len(player_1_cards) > 0 and len(player_2_cards) > 0:
        if get_round_hash(player_1_cards, player_2_cards) in previous_rounds:
            return (1, player_1_cards)
        previous_rounds.add(get_round_hash(player_1_cards, player_2_cards))
        player_1_card = player_1_cards.pop(0)
        player_2_card = player_2_cards.pop(0)
        roundwinner = None
        if player_1_card <= len(player_1_cards) and player_2_card <= len(player_2_cards):
            roundwinner = play_recursive_game(
                player_1_cards[:player_1_card].copy(), player_2_cards[:player_2_card].copy(), set())[0]
        else:
            roundwinner = 1 if player_1_card > player_2_card else 2
        if roundwinner == 1:
            player_1_cards.append(player_1_card)
            player_1_cards.append(player_2_card)
        else:
            player_2_cards.append(player_2_card)
            player_2_cards.append(player_1_card)
    if len(player_1_cards) == 0:
        return (2, player_2_cards)
    if len(player_2_cards) == 0:
        return (1, player_1_cards)


def play_game_2():
    _, cards = play_recursive_game(
        player_cards[1].copy(), player_cards[2].copy())
    return count_points(cards)


# Task 1
print(play_game_1())


# Task 2
print(play_game_2())
