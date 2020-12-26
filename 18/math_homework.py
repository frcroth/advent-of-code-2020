with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]


def tokenize(line):
    initial_tokens = list(line)
    tokens = []
    for token in initial_tokens:
        tokens.append(token)
        if token == ')' or token == '(':
            tokens.append(' ')
    tokens = list(filter((lambda x: x != ' '), tokens))
    return tokens


def merge(tokens):
    # tokens may not include ( or )
    result = 0
    current_action = (lambda a, b: a + b)
    for token in tokens:
        if token == '+':
            current_action = (lambda a, b: a + b)
        elif token == '*':
            current_action = (lambda a, b: a * b)
        else:
            result = current_action(result, int(token))
    return result


def merge_with_precedence(tokens):
    # tokens may not include ( or )
    # calculate addition
    while '+' in tokens:
        for i, token in enumerate(tokens):
            if token == '+':
                addend_1 = tokens.pop(i-1)
                addend_2 = tokens.pop(i-1)
                tokens.insert(i-1, int(addend_1) + int(addend_2))
                break
    return merge(tokens)


def remove_brackets(tokens, use_precedence=False):
    # calculate things in brackets
    bracket_level = 0
    brackets_level = []
    for i, token in enumerate(tokens):
        if token == '(':
            bracket_level += 1
        if token == ')':
            bracket_level -= 1
            end = i
            start = brackets_level.index(bracket_level+1)
            # tokens from end to start are in the same brackets, lowest level
            if use_precedence:
                partial_result = merge_with_precedence(tokens[start+1:end])
            else:
                partial_result = merge(tokens[start+1:end])
            new_list = tokens[:start] + [partial_result] + tokens[end+1:]
            return new_list
        brackets_level.append(bracket_level)
    return tokens


def calculate(tokens, use_precedence=False):
    while '(' in tokens or ')' in tokens:
        tokens = remove_brackets(tokens, use_precedence)
    if use_precedence:
        result = merge_with_precedence(tokens)
    else:
        result = merge(tokens)
    return result


def task_1():
    sum = 0
    for line in content:
        sum += calculate(tokenize(line), False)
    return sum


def task_2():
    sum = 0
    for line in content:
        sum += calculate(tokenize(line), True)
    return sum


print(task_1())

print(task_2())
