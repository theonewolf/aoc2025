#!/usr/bin/env python3

# brute force
# generate numbers
# check digits; if even
# and if first half equal second half
# add to running total

if __name__ == '__main__':
    summation = 0
    with open('input') as data:
        for line in data.readlines():
            ranges = line.strip().split(',')

            for r in ranges:
                start, stop = r.split('-')

                for number in range(int(start), int(stop) + 1):
                    strnumber = str(number)
                    if len(strnumber) % 2 == 0:
                        mid = len(strnumber) // 2
                        part1, part2 = int(strnumber[:mid]), int(strnumber[mid:])

                        if part1 == part2:
                            summation += number

    print(f'{summation}')
