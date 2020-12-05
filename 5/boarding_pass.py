with open('input.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]


def translate(boarding_string):
    row = boarding_string[:7]
    col = boarding_string[7:]
    row = row.replace("F", "0")
    row = row.replace("B", "1")
    col = col.replace("L","0")
    col = col.replace("R","1")
    return int(row, base=2), int(col, base=2)

def seat_id(boarding_string):
    row, col = translate(boarding_string)
    return row * 8 + col

# Task 1
def get_max_id():
    boarding_ids = map(seat_id, content)
    return max(boarding_ids)

# Task 2
def get_missing_seat():
    boarding_ids = map(seat_id, content)
    seats = sorted(boarding_ids)
    for seat in seats:
        if seat+1 not in seats:
            return seat+1
