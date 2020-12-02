def conforms_r1(password, char, num1, num2):
    count = password.count(char)
    return num1 <= count <= num2

def conforms_r2(password, char, num1, num2):
    return (password[num1-1] == char) != (password[num2-1] == char)

with open("input.txt") as f:
    content = f.readlines()

content = [x.strip() for x in content]

valid_count_rule1 = 0
valid_count_rule2 = 0

for line in content:
    rule = line.split(':')[0]
    num1 = int(rule.split('-')[0])
    num2 = int(rule.split('-')[1].split(' ')[0])
    char = rule.split('-')[1].split(' ')[1]
    password = line.split(':')[1].strip()
    if conforms_r1(password, char, num1, num2):
        valid_count_rule1 += 1
    if conforms_r2(password, char, num1, num2):
        valid_count_rule2 += 1

print(valid_count_rule1)
print(valid_count_rule2)