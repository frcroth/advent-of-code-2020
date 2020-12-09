with open('input.txt') as f:
    content = f.readlines()

content = [int(x.strip()) for x in content]


def any_pair_sums_to(numbers, sum):
    for (index, num) in enumerate(numbers):
        for (index2, num2) in enumerate(numbers):
            if num + num2 == sum and index != index2:
                return True
    return False


def find_first_wrong_number():
    current_numbers = content[:25]
    for num in content[25:]:
        if any_pair_sums_to(current_numbers, num):
            current_numbers.pop(0)
            current_numbers.append(num)
        else:
            return num


def find_sub_array_with_sum(array, sum):
    for i in range(len(array)):
        current_sum = array[i]
        j = i + 1
        while j <= len(array):
            if current_sum == sum:
                return (i, j-1)
            if current_sum > sum or j == len(array):
                break
            current_sum = current_sum + array[j]
            j += 1
    return -1


def break_encryption():
    wrong_number = find_first_wrong_number()
    start, end = find_sub_array_with_sum(content, wrong_number)
    smallest = min(content[start:end])
    largest = max(content[start:end])
    return smallest + largest

# Part 1
print(find_first_wrong_number())

# Part 2
print(break_encryption())
