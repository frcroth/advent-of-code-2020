import itertools

with open('input.txt') as f:
    content = f.readlines()

content = [int(x.strip()) for x in content]


# Base
content.append(0)

# Device
content.append(max(content) + 3)

content.sort()


def get_diffs():
    diff1 = []
    diff2 = []
    diff3 = []

    for i in range(len(content)):
        if i < len(content)-1:
            diff = content[i+1] - content[i]
            if diff == 3:
                diff3.append(content[i])
            if diff == 2:
                diff2.append(content[i])
            if diff == 1:
                diff1.append(content[i])
    return diff1, diff2, diff3


def task1():
    diff1, diff2, diff3 = get_diffs()
    return len(diff1) * len(diff3)


def task2():

    diff1, diff2, diff3 = get_diffs()
    # all numbers with difference 3 must be part of every solution
    # --> Separate into parts that are 3 apart --> edges are part of any solution
    parts = []
    current_array = []
    for i in range(len(content)):
        if content[i-1] in diff3:
            parts.append(current_array)
            current_array = []
        current_array.append(content[i])

    # since in the gaps in each part are always 1 apart and max part length is only 5
    # we just need to check if the list has a length of more than 4 or not.
    # If not, we don't need to include any adapter, else 1
    result = 1
    for part in parts:
        result *= brute_force_part(part)
    return result


def brute_force_part(part):
    # given a list of numbers, max difference 2
    if len(part) < 3:
        return 1
    if len(part) == 3:
        return 2
    if len(part) == 4:
        return 4  # make use of knowledge that they are at most 1 a part in every part
    # remove edges
    part.pop(0)
    part.pop(len(part)-1)

    combinations = get_combinations(part)

    # test combinations
    count = 0
    for combination in combinations:
        if len(combination) > 1:
            max_diff = max([combination[i+1]-combination[i]
                            for i in range(len(combination)-1) if combination[i] < combination[i+1]])
        else:
            max_diff = 0
        if max_diff <= 3:
            count += 1
    return count


def get_combinations(arr):
    combinations = []
    for i in range(1, len(arr)+1):
        combinations += list(itertools.combinations(arr, i))
    return [list(element) for element in combinations]


print(task1())

print(task2())
