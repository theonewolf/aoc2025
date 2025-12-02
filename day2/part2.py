#!/usr/bin/env python3

if __name__ == '__main__':
    summation = 0
    with open('input') as data:
        for line in data.readlines():
            ranges = line.strip().split(',')

            for r in ranges:
                start, stop = r.split('-')

                for number in range(int(start), int(stop) + 1):
                    strnumber = str(number)
                    
                    for j in range(1, len(strnumber) // 2 + 1):
                        seq1 = strnumber[:j]
                        match = True

                        if len(strnumber) % j != 0:
                            continue

                        for i in range(len(strnumber) // j):
                            seq = strnumber[i * j : i * j + j]
                            if seq1 != seq:
                                match = False
                                break

                        if match:
                            summation += number
                            break

    print(f'{summation}')
