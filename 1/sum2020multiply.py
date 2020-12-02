with open("input.txt") as f:
    content = f.readlines()

content = [int(x.strip()) for x in content]

look_for_three = True

if lookforthree:
    for num1 in content:
        for num2 in content:
            for num3 in content:
                if num1 + num2 + num3 == 2020:
                    print(num1 * num2 * num3)


else:
    for num1 in content:
        for num2 in content:
            if num1 + num2 == 2020:
                print(num1 * num2)
