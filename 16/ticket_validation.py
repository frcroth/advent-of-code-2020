import re

with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]


def parse_content(content):
    possible_valid_numbers = set()

    ticket_count = 0
    error_rate = 0
    your_ticket = ""
    rules_dict = dict()
    valid_tickets = list()

    mode = 'rules'
    for line in content:
        if line == "" and mode == 'your ticket':
            mode = 'nearby tickets'
            continue
        if line == "" and mode == 'rules':
            mode = 'your ticket'
            continue
        if mode == 'rules':
            rule_pairs = re.findall(r"[0-9]*\-[0-9]*", line)
            rule_name = line.split(':')[0]
            valid_numbers = set(range(int(rule_pairs[0].split('-')[0]),
                                      int(rule_pairs[0].split('-')[1])+1))
            valid_numbers = valid_numbers.union(
                set(range(int(rule_pairs[1].split('-')[0]),
                          int(rule_pairs[1].split('-')[1])+1)))
            possible_valid_numbers = possible_valid_numbers.union(
                valid_numbers)
            rules_dict[rule_name] = valid_numbers
        if mode == 'your ticket':
            if line == 'nearby tickets:':
                continue
            else:
                your_ticket = line
        if mode == 'nearby tickets':
            if line == 'nearby tickets:':
                continue

            ticket_count += 1
            numbers = line.split(',')
            valid = True
            for number in numbers:
                if int(number) not in possible_valid_numbers:
                    error_rate += int(number)
                    valid = False
            if valid:
                valid_tickets.append(line)

    return {"error_rate": error_rate,
            "valid_tickets": valid_tickets,
            "rules_dict": rules_dict,
            "your_ticket": your_ticket}


def fix_rules(rule_sets, fixed_rules):
    for i in range(len(rule_sets)):
        rule_set = rule_sets[i]
        if type(rule_set) is not set:
            fixed_rules.add(rule_set)
            continue
        else:
            if len(rule_set) == 1:
                rule_sets[i] = list(rule_set)[0]
                fixed_rules.add(list(rule_set)[0])
            else:
                rule_sets[i] = rule_sets[i].difference(fixed_rules)
    if len(fixed_rules) == len(rule_sets):
        return rule_sets
    else:
        return fix_rules(rule_sets, fixed_rules)


def match_rules():
    valid_tickets = parse_content(content)["valid_tickets"]
    rules_dict = parse_content(content)["rules_dict"]
    rules_tickets_match = [set(rules_dict.keys())] * \
        len(valid_tickets[0].split(','))
    for ticket in valid_tickets:
        numbers = ticket.split(',')
        i = 0
        for number in numbers:
            possible_rules = set()
            for rule_name, possible_values in rules_dict.items():
                if int(number) in possible_values:
                    possible_rules.add(rule_name)
            rules_tickets_match[i] = rules_tickets_match[i].intersection(
                possible_rules)
            i += 1
    return fix_rules(rules_tickets_match, set())


def task_2():
    rules = match_rules()
    your_ticket = parse_content(content)["your_ticket"]
    ticket_values = your_ticket.split(',')
    result = 1
    for i, rule in enumerate(rules):
        if rule.startswith("departure"):
            result *= int(ticket_values[i])
    return result


# Task 1
print(parse_content(content)["error_rate"])

# Task 2
print(task_2())
