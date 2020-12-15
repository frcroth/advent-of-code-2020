with open('input1.txt') as f:
    content = f.readlines()

numbers = [int(x.strip()) for x in content]
number_dict = dict()

for i in range(len(numbers)):
    number_dict[numbers[i]] = i


def play_game(play_count):
    for i in range(len(numbers), play_count):
        last_number = numbers[i-1]
        if last_number not in number_dict:
            numbers.append(0)
            number_dict[last_number] = i-1
            continue
        prev_occurrence = number_dict[last_number]
        diff = (i-1) - prev_occurrence
        numbers.append(diff)
        number_dict[last_number] = i-1
        continue

    return numbers


def task_1():
    print(play_game(2020)[-1])


def task_2():
    print(play_game(30000000)[-1])


task_1()

task_2()
