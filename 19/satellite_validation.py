
def read_input():
    with open('input.txt') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    mode = "rules"
    rule_dict = dict()
    test_strings = list()
    for line in content:
        if mode == "rules" and line == "":
            mode = "strings"
            continue
        if mode == "rules":
            rule_num = line.split(":")[0]
            if '"' in line:
                # literal rule
                value = line.split('"')[1]
                rule_dict[rule_num] = ("literal", value)
            elif '|' in line:
                value1 = line.split(":")[1].split('|')[0].strip().split(' ')
                value2 = line.split(":")[1].split('|')[1].strip().split(' ')
                rule_dict[rule_num] = ("optional", value1, value2)
            else:
                value = line.split(":")[1].strip().split(' ')
                rule_dict[rule_num] = ("direct", value)
        if mode == "strings":
            test_strings.append(line)
    return rule_dict, test_strings


def combine_rec(list_of_sets):
    if list_of_sets is None:
        return []
    current_set = list_of_sets[0]
    results = set()
    if len(list_of_sets) == 1:
        return list(list_of_sets[0])
    for string in list(current_set):
        options = combine_rec(list_of_sets[1:])
        for option in options:
            results.add(string + option)
    return results


def get_string_set(rule_numbers, fixed_rule_dict):
    #print("get string set for numbers " + str(rule_numbers))
    sequence = []
    for num in rule_numbers:
        sequence.append(fixed_rule_dict[num])
    #print("calculating combinations of " + str(sequence))
    solutions = combine_rec(sequence)
    if type(solutions) is not set:
        return set(solutions)
    #print("got string set for numbers " + str(rule_numbers) + ", it's " + str(solutions))
    return solutions


def build_strings(rule_dict, task_2=False):
    loop_depth = 10
    fixed_rule_dict = dict()
    for rule_num, rule in rule_dict.items():
        if rule_dict[rule_num][0] == "literal":
            fixed_rule_dict[rule_num] = set(rule_dict[rule_num][1])
    while len(fixed_rule_dict.keys()) < len(rule_dict):
        for rule_num, rule in rule_dict.items():
            # print(fixed_rule_dict)
            if rule[0] == "direct" and not rule_num in fixed_rule_dict:
                may_be_solved = True
                for num in rule[1]:
                    if num not in fixed_rule_dict:
                        may_be_solved = False
                        break
                if may_be_solved:
                    solutions = get_string_set(rule[1], fixed_rule_dict)
                    fixed_rule_dict[rule_num] = solutions
                if rule_num == '8' and task_2 and may_be_solved:
                    for i in range(loop_depth):
                        solutions = get_string_set(['42','8'], fixed_rule_dict)
                        fixed_rule_dict[rule_num] = fixed_rule_dict[rule_num].union(solutions)
                if rule_num == '11' and task_2 and may_be_solved:
                    for i in range(loop_depth):
                        solutions = get_string_set(['42','11','31'], fixed_rule_dict)
                        fixed_rule_dict[rule_num] = fixed_rule_dict[rule_num].union(solutions)
            if rule[0] == "optional" and not rule_num in fixed_rule_dict:
                may_be_solved = True
                for num in rule[1]:
                    if num not in fixed_rule_dict:
                        may_be_solved = False
                        break
                for num in rule[2]:
                    if num not in fixed_rule_dict:
                        may_be_solved = False
                        break
                if may_be_solved:
                    solution1 = get_string_set(rule[1], fixed_rule_dict)
                    solution1 = solution1.union(
                        get_string_set(rule[2], fixed_rule_dict))
                    fixed_rule_dict[rule_num] = set(solution1)
    return fixed_rule_dict


def get_correct_strings(rule_dict, task_2=False):
    return build_strings(rule_dict, task_2)['0']


def get_number_of_matching_strings(correct_strings, input_strings):
    correct_sum = 0
    for input_str in input_strings:
        if input_str in correct_strings:
            correct_sum += 1
    return correct_sum


def calc_task(task_2=False):
    rule_dict, test_strings = read_input()
    correct_strings = get_correct_strings(rule_dict, task_2)
    return get_number_of_matching_strings(correct_strings, test_strings)


# Task 1
print(calc_task())

# Task 2
print(calc_task(True))
