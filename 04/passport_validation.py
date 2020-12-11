import re

with open('input.txt') as f:
    content = f.readlines()

# identify passports

passports = []
current_passport = ""
for line in content:
    if line[0] == '\n':
        passports.append(current_passport.strip())
        current_passport = ""
    else:
        current_passport = current_passport + " " + line.strip()
# last passport
passports.append(current_passport.strip())


# validate passports


def get_passport_dict(passport):
    data = dict()
    pairs = re.findall(r"[a-z]{3}:[#a-z0-9]*", passport)
    for pair in pairs:
        data[pair.split(':')[0]] = pair.split(':')[1]
    return data


valid_count1 = 0


def check_validity1(passport):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    data = get_passport_dict(passport)
    valid = True
    for field in required_fields:
        if field not in data:
            valid &= False
    return valid


valid_count2 = 0


def check_validity2(passport):
    data = get_passport_dict(passport)
    if not 1920 <= int(data["byr"]) <= 2002:
        # print(passport + " is not valid because of birth year")
        return False
    if not 2010 <= int(data["iyr"]) <= 2020:
        # print(passport + " is not valid because of issue year")
        return False
    if not 2020 <= int(data["eyr"]) <= 2030:
        # print(passport + " is not valid because of expiration year")
        return False
    if 'cm' in data["hgt"]:
        if not 150 <= int(data["hgt"].split('c')[0]) <= 193:
            # print(passport + " is not valid because of height (cm)")
            return False
    elif 'in' in data["hgt"]:
        if not 59 <= int(data["hgt"].split('i')[0]) <= 76:
            # print(passport + " is not valid because of height (in)")
            return False
    else:
        return False
    if not data["hcl"][0] == '#':
        # print(passport + " is not valid because of hair color (missing #)")
        return False
    for char in data['hcl'][1:]:
        if char not in "0123456789abcdef":
            # print(passport + " is not valid because of hair color")
            return False
    if not data['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        # print(passport + " is not valid because of eye color")
        return False
    if not len(data['pid']) == 9:
        # print(passport + " is not valid because of pid (length not right)")
        return False
    for char in data['pid'][1:]:
        if char not in "0123456789":
            # print(passport + " is not valid because of pid (non valid chars)")
            return False

    return True


for passport in passports:
    if check_validity1(passport):
        valid_count1 += 1
        if check_validity2(passport):
            valid_count2 += 1

print("Valid passports (fields exist):" + str(valid_count1))
print("Valid passports (fields are validated):" + str(valid_count2))
