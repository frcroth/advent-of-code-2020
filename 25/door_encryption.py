with open('input.txt') as f:
    content = f.readlines()
content = [int(x.strip()) for x in content]

card_public_key = content[0]
door_public_key = content[1]


def generate_public_key(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


def brute_force_loop_size(public_key):
    subject_number = 7
    value = 1
    for i in range(1, 100000000):
        value *= subject_number
        value = value % 20201227
        if value == public_key:
            return i
    print("No loop size found")


def task_1():
    card_loop_size = brute_force_loop_size(card_public_key)
    door_loop_size = brute_force_loop_size(door_public_key)
    encryption_key = generate_public_key(door_public_key, card_loop_size)
    assert(encryption_key == generate_public_key(
        card_public_key, door_loop_size))
    return encryption_key


# Task 1
print(task_1())
