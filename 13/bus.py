from functools import reduce
import math

with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]

current_time = int(content[0])
busses = content[1].split(',')

bus_ids = []

for bus in busses:
    if bus != "x":
        bus_ids.append(int(bus))

bus_ids.sort()


def get_next_bus(time, bus_id):
    return math.ceil(time/bus_id)*bus_id


def get_wait_time(time, bus_id):
    return get_next_bus(time, bus_id) - time


def task_1():
    bus_waiting_times = []
    for bus in bus_ids:
        bus_waiting_times.append((bus, get_wait_time(current_time, bus)))
    next_bus = min(bus_waiting_times, key=lambda t: t[1])
    return next_bus[0] * next_bus[1]


def task_2():
    n = []
    remainders = []
    for i in range(len(busses)):
        if busses[i] != 'x':
            bus_id = int(busses[i])
            remainders.append((bus_id-i) % bus_id)
            n.append(bus_id)
    return chinese_remainder(n, remainders)

# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


print(task_1())

print(task_2())
