import string

with open('input.txt') as f:
    content = f.readlines()

# identify groups

groups = []
current_group = ""
for line in content:
    if line[0] == '\n':
        groups.append(current_group.strip())
        current_group = ""
    else:
        if len(current_group) < 1:
            current_group = line.strip()
        else:
            current_group = current_group + "\n" + line.strip()
# last group
groups.append(current_group)


def get_unique_chars(group):
    return list(set(group.replace("\n", "").replace(" ", "")))


def get_common_chars(group):
    common_chars = list(string.ascii_lowercase)
    for passenger in group.split('\n'):
        if passenger:
            # Intersection
            common_chars = list(set(common_chars) & set(passenger))
    return common_chars


def get_char_count(group):
    return len(get_unique_chars(group))


def get_sum_of_counts():
    sum = 0
    for group in groups:
        sum += get_char_count(group)
    return sum


def get_common_count(group):
    return len(get_common_chars(group))


def get_sum_of_common_counts():
    sum = 0
    for group in groups:
        sum += get_common_count(group)
    return sum


# Task 1
print(get_sum_of_counts())

# Task 2
print(get_sum_of_common_counts())
