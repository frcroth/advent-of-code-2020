import re

with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]


def task_1():
    memory = dict()
    current_bitmask = "X" * 36

    for line in content:
        if line.startswith("mask"):
            current_bitmask = line.split('=')[1].strip()
        if line.startswith("mem"):
            address = re.findall(r"\[[0-9]*\]", line)[0][1:][:-1]
            value = line.split("=")[1].strip()
            binary_value = "{0:b}".format(int(value))
            binary_value = bin_pad(binary_value, 36)
            effective_binary_value = ""
            for i in range(36):
                if current_bitmask[i] == 'X':
                    effective_binary_value += binary_value[i]
                if current_bitmask[i] == '0' or current_bitmask[i] == '1':
                    effective_binary_value += current_bitmask[i]
            memory[address] = effective_binary_value
    return memory


def bin_pad(value, length):
    while len(value) < length:
        value = "0" + value
    return value


def task_2():
    memory = dict()
    current_bitmask = "X" * 36
    for line in content:
        if line.startswith("mask"):
            current_bitmask = line.split('=')[1].strip()
        if line.startswith("mem"):
            address = re.findall(r"\[[0-9]*\]", line)[0][1:][:-1]
            binary_address = "{0:b}".format(int(address))
            binary_address = bin_pad(binary_address, 36)
            value = line.split("=")[1].strip()
            addresses = get_addresses(binary_address, current_bitmask)
            for adr in addresses:
                memory[adr] = value
    return memory


def get_addresses(address, mask):
    effective_address = ""
    for i in range(36):
        if mask[i] == 'X':
            effective_address += 'X'
        if mask[i] == '0':
            effective_address += address[i]
        if mask[i] == '1':
            effective_address += '1'
    floating_count = effective_address.count('X')

    result = [effective_address]
    for i in range(floating_count):
        address_list = []
        for addr in result:
            floating_position = addr.index('X')
            address_list.append(
                addr[:floating_position] + '1' + addr[floating_position+1:])
            address_list.append(
                addr[:floating_position] + '0' + addr[floating_position+1:])
        result = address_list
    return result


def get_sum(memory, base=10):
    sum = 0
    for key, value in memory.items():
        sum += int(value, base)
    return sum


print(get_sum(task_1(), 2))

print(get_sum(task_2()))
