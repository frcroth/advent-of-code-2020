with open('input.txt') as f:
    content = f.readlines()

matrix = [x.strip() for x in content]

points = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
number_of_trees = [0, 0, 0, 0, 0]

width = len(matrix[0])


def iteration():
    for i in range(len(slopes)):
        points[i] = (points[i][0] + slopes[i][0]) % width,\
                     points[i][1] + slopes[i][1]
        if points[i][1] <= len(matrix) - 1:
            if matrix[points[i][1]][points[i][0]] == '#':
                number_of_trees[i] += 1


def all_done():
    all_done = True
    for i in range(len(slopes)):
        all_done &= points[i][1] > len(matrix) - 1
    return all_done


while True:
    iteration()
    if all_done():
        break

multiplied = 1
for i in range(len(slopes)):
    print("Tree number for slope " + str(i) +
          " with " + str(number_of_trees[i]))
    multiplied *= number_of_trees[i]

print(multiplied)
