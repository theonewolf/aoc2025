#!/usr/bin/env python3

if __name__ == '__main__':
    with open('input') as data:
        maximums = []

        for line in data.readlines():
            line = line.strip()
            digits = [int(c) for c in line]

            maximum = 0
            for i, d in enumerate(digits):
                for d2 in digits[i+1:]:
                    if d * 10 + d2 > maximum:
                        maximum = d * 10 + d2
            maximums.append(maximum)

        print(f'{sum(maximums)=}')
