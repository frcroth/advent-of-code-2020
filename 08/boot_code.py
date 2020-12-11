with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]


def parse_line(line):
    operation = line.split(' ')[0]
    value = int(line.split(' ')[1])
    return operation, value


def parse_input(input):
    code = []
    for line in input:
        parsed = parse_line(line)
        code.append(parsed)
    return code


def change_statement(pos, new_statement, code):
    code = code.copy()
    code[pos] = (new_statement, code[pos][1])
    return code


def swap_and_check(code):
    nop_positions = [index for (index, statement) in enumerate(
        code) if statement[0] == 'nop']
    jmp_positions = [index for (index, statement) in enumerate(
        code) if statement[0] == 'jmp']
    for nop_position in nop_positions:
        changed_code = change_statement(nop_position, "jmp", code)
        result = execute(changed_code)
        if "Done" in result:
            return result.split(":")[1]
    for jmp_position in jmp_positions:
        changed_code = change_statement(jmp_position, "nop", code)
        result = execute(changed_code)
        if "Done" in result:
            return result.split(":")[1]
    return "No swap successful"


def execute(code):
    hit_lines = set()
    accumulator = 0
    instruction_pointer = 0
    while True:
        hit_lines.add(instruction_pointer)
        statement = code[instruction_pointer]
        if statement[0] == 'nop':
            next_line = instruction_pointer + 1
        if statement[0] == 'acc':
            accumulator += statement[1]
            next_line = instruction_pointer + 1
        if statement[0] == 'jmp':
            next_line = instruction_pointer + statement[1]

        if next_line in hit_lines:
            return "Error on loop with:" + str(accumulator)
        instruction_pointer = next_line
        if next_line == len(code):
            return "Done:" + str(accumulator)


# Task 1
print(execute(parse_input(content)))

# Task 2
print(swap_and_check(parse_input(content)))
