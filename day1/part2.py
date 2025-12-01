#!/usr/bin/env python3

start = 50
maximum = 100
password = 0

if __name__ == '__main__':

    with open ('input') as data:
        for line in data.readlines():
            direction = line[0]
            distance = int(line[1:])

            print(f'{direction=} {distance=}')

            match direction:
                case 'L':
                    if not start:
                        start -= distance
                        zeros, start = divmod(start, maximum)
                        print(f'\tnot start, adding {abs(zeros)-1=}')
                        password += abs(zeros) - 1
                    else:
                        start -= distance
                        zeros, start = divmod(start, maximum)
                        print(f'\tstart, adding {abs(zeros)}')
                        password += abs(zeros) + int(not start)
                case 'R':
                    start += distance
                    zeros, start = divmod(start, maximum)
                    print(f'\tadding {zeros=}')
                    password += zeros
                case _:
                    raise Exception(f'Invalid value: "{distance}"')

    print(f'{password=}')
