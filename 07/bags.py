with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]

bag_dict = dict()


def parse_rule(rule):
    bags_contained = []
    bag = rule.split('contain')[0].strip().split('bag')[0].strip()
    for containing_bag in rule.split('contain')[1].split(','):
        containing_bag = containing_bag.strip()
        if containing_bag.strip() == "no other bags.":
            return bag, []
        num = containing_bag.split(' ')[0]
        name = ' '.join(containing_bag.split(' ')[1:3])
        bags_contained.append((int(num), name))
    return bag, bags_contained


def build_dict():
    for line in content:
        bag, bags_contained = parse_rule(line)
        bag_dict[bag] = bags_contained


def find_bags_containing(bag_color):
    result_bags = []
    for key, value in bag_dict.items():
        for item in value:
            if item[1] == bag_color:
                result_bags.append(key)
    return result_bags


def find_bags_containing_recursive(bag_color):
    result_bags = set()
    find_queue = [bag_color]
    searched_elements = set()
    while len(find_queue) > 0:
        search_element = find_queue[0]
        find_queue.remove(search_element)
        searched_elements.add(search_element)
        found_bags = find_bags_containing(search_element)
        for bag in found_bags:
            if bag not in searched_elements:
                find_queue.append(bag)
            result_bags.add(bag)
    return result_bags


def count_bags(bag_color):
    sum = 1
    if len(bag_dict[bag_color]) == 0:
        return 1
    for item in bag_dict[bag_color]:
        sum += item[0] * count_bags(item[1])
    return sum


build_dict()

# Task 1
print(len(find_bags_containing_recursive('shiny gold')))

# Task 2
print(count_bags('shiny gold')-1)
