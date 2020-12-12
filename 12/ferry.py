import math

with open('input.txt') as f:
    content = f.readlines()

actions = [(x.strip()[0], x.strip()[1:]) for x in content]


def normalize_angle(angle):
    if 0 <= angle < 360:
        return angle
    elif angle < 0:
        return normalize_angle(angle+360)
    elif angle >= 360:
        return normalize_angle(angle - 360)


def task1():
    position = (0, 0)
    angle = 0

    for action in actions:
        if action[0] == "N":
            position = (position[0], position[1] - int(action[1]))
        if action[0] == "S":
            position = (position[0], position[1] + int(action[1]))
        if action[0] == "W":
            position = (position[0] - int(action[1]), position[1])
        if action[0] == "E":
            position = (position[0] + int(action[1]), position[1])
        if action[0] == "F":
            if angle == 0:  # east
                position = (position[0] + int(action[1]), position[1])
            if angle == 90:  # north
                position = (position[0], position[1] - int(action[1]))
            if angle == 180:  # west
                position = (position[0] - int(action[1]), position[1])
            if angle == 270:  # south
                position = (position[0], position[1] + int(action[1]))
        if action[0] == "L":
            angle = normalize_angle(angle + int(action[1]))
        if action[0] == "R":
            angle = normalize_angle(angle - int(action[1]))

    print(manhattan(position))


def task2():
    ship_position = (0, 0)
    waypoint_position = (10, -1)

    for action in actions:
        if action[0] == "N":
            waypoint_position = (
                waypoint_position[0], waypoint_position[1] - int(action[1]))
        if action[0] == "S":
            waypoint_position = (
                waypoint_position[0], waypoint_position[1] + int(action[1]))
        if action[0] == "W":
            waypoint_position = (
                waypoint_position[0] - int(action[1]), waypoint_position[1])
        if action[0] == "E":
            waypoint_position = (
                waypoint_position[0] + int(action[1]), waypoint_position[1])
        if action[0] == "F":
            ship_position = (ship_position[0] + int(action[1]) * waypoint_position[0],
                             ship_position[1] + int(action[1]) * waypoint_position[1])
        if action[0] == "L":
            angle = int(action[1])
            if angle == 90:
                waypoint_position = (
                    waypoint_position[1], - waypoint_position[0])
            if angle == 180:
                waypoint_position = (
                    - waypoint_position[0], - waypoint_position[1])
            if angle == 270:
                waypoint_position = (-waypoint_position[1],
                                     waypoint_position[0])

        if action[0] == "R":
            angle = int(action[1])
            if angle == 270:
                waypoint_position = (
                    + waypoint_position[1], - waypoint_position[0])
            if angle == 180:
                waypoint_position = (
                    - waypoint_position[0], - waypoint_position[1])
            if angle == 90:
                waypoint_position = (-waypoint_position[1],
                                     waypoint_position[0])

    print(manhattan(ship_position))


def manhattan(position):
    return abs(position[0]) + abs(position[1])


task1()

task2()
