import re


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


def build_strings(rule_dict, task_2=False):
    loop_depth = 3  # tested, 3 was the lowest for my input
    fixed_rule_dict = dict()
    for rule_num, rule in rule_dict.items():
        if rule_dict[rule_num][0] == "literal":
            fixed_rule_dict[rule_num] = rule_dict[rule_num][1]
    while len(fixed_rule_dict.keys()) < len(rule_dict):
        for rule_num, rule in rule_dict.items():
            if rule[0] == "direct" and not rule_num in fixed_rule_dict:
                may_be_solved = True
                for num in rule[1]:
                    if num not in fixed_rule_dict:
                        may_be_solved = False
                        break
                if may_be_solved:
                    solution = ""
                    for num in rule[1]:
                        solution += fixed_rule_dict[num]
                    fixed_rule_dict[rule_num] = "(" + solution + ")"
                if rule_num == '8' and task_2 and may_be_solved:
                    for _ in range(loop_depth):
                        prev_solution = fixed_rule_dict[rule_num]
                        fixed_rule_dict[rule_num] = "(" + prev_solution + \
                            "|" + prev_solution + prev_solution + ")"
                if rule_num == '11' and task_2 and may_be_solved:
                    for _ in range(loop_depth):
                        prev_solution = fixed_rule_dict[rule_num]
                        fixed_rule_dict[rule_num] = "(" + prev_solution + "|" + \
                            fixed_rule_dict['42'] + prev_solution + \
                            fixed_rule_dict['31'] + ")"
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
                    solution1 = ""
                    for num in rule[1]:
                        solution1 += fixed_rule_dict[num]
                    solution2 = ""
                    for num in rule[2]:
                        solution2 += fixed_rule_dict[num]
                    fixed_rule_dict[rule_num] = "(" + \
                        solution1 + "|" + solution2 + ")"
    return fixed_rule_dict


def get_complete_regex(rule_dict, task_2=False):
    return build_strings(rule_dict, task_2)['0']


def get_number_of_matching_strings(regex, input_strings):
    correct_sum = 0
    correct_regex = re.compile(regex)
    for input_str in input_strings:
        if correct_regex.fullmatch(input_str) is not None:
            correct_sum += 1
    return correct_sum


def calc_task(task_2=False):
    rule_dict, test_strings = read_input()
    correct_strings = get_complete_regex(rule_dict, task_2)
    return get_number_of_matching_strings(correct_strings, test_strings)


# Task 1
print(calc_task())

# Task 2
print(calc_task(True))
