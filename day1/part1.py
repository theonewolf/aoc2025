#!/usr/bin/env python3

start = 50
maximum = 100
password = 0

if __name__ == '__main__':

    with open ('input') as data:
        for line in data.readlines():
            direction = line[0]
            distance = int(line[1:])

            match direction:
                case 'L':
                    start -= distance
                case 'R':
                    start += distance
                case _:
                    raise Exception(f'Invalid value: "{distance}"')

            start %= maximum

            if not start:
                password += 1

    print(f'{password=}')
