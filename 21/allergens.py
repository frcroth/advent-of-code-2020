from operator import itemgetter

with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]
food = []
for line in content:
    ingredients = line.split('(')[0].strip().split(' ')
    allergens = line.split('contains ')[1][:-1].split(', ')
    food.append((ingredients, allergens))


def get_allergens():
    allergens = []
    for f in food:
        allergens.extend(f[1])
    return list(set(allergens))


def get_all_ingredients():
    ingredients = []
    for f in food:
        ingredients.extend(f[0])
    return list(set(ingredients))


def get_possible_values_for_allergen(allergen):
    ingredients = set(get_all_ingredients())
    for f in food:
        if allergen in f[1]:
            ingredients = ingredients.intersection(set(f[0]))
    return list(ingredients)


def get_ingredients_without_allergens():
    ingredients = set(get_all_ingredients())
    for allergen in get_allergens():
        possible_ingredients = get_possible_values_for_allergen(allergen)
        ingredients = ingredients - set(possible_ingredients)
    return list(ingredients)


def count_appearance_of_ingredient(ingredient):
    count = 0
    for f in food:
        if ingredient in f[0]:
            count += 1
    return count


def task_1():
    total_count = 0
    ingredients = get_ingredients_without_allergens()
    for i in ingredients:
        total_count += count_appearance_of_ingredient(i)
    return total_count


def get_ingredients_for_allergents():
    # Remove impossible values
    all_allergents = get_allergens()
    ingredients = get_ingredients_without_allergens()
    ingredient_allergent_list = food.copy()
    for i, f in enumerate(ingredient_allergent_list):
        ingredient_allergent_list[i] = (
            list(set(f[0]) - set(ingredients)), f[1])

    # fixed allergens <-> ingredients
    allergen_dict = dict()
    while len(all_allergents) > len(allergen_dict):
        for i, f in enumerate(ingredient_allergent_list):
            if len(f[0]) == 1 and len(f[1]) == 1:
                allergen_dict[f[1][0]] = f[0][0]
        for allergent in all_allergents:
            if allergent not in allergen_dict:
                ingredients_for_allergent = set(
                    get_possible_values_for_allergen(allergent))
                for i, f in enumerate(ingredient_allergent_list):
                    if allergent in f[1]:
                        ingredients_for_allergent = ingredients_for_allergent.intersection(
                            set(f[0]))
                if len(ingredients_for_allergent) == 1:
                    allergen_dict[allergent] = list(
                        ingredients_for_allergent)[0]
        # remove fixed pairs
        for i, f in enumerate(ingredient_allergent_list):
            ingredient_allergent_list[i] = (list(set(
                f[0]) - set(allergen_dict.values())), list(set(f[1]) - set(allergen_dict.keys())))
    return allergen_dict


def arrange_ingredients():
    pairs = list(get_ingredients_for_allergents().items())
    pairs = sorted(pairs, key=itemgetter(0))
    allergens = list(map((lambda item: item[1]), pairs))
    return ','.join(allergens)


# Task 1
print(task_1())

# Task 2
print(arrange_ingredients())
