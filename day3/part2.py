#!/usr/bin/env python3

from tqdm import tqdm

# this does work, confirmed on the small sample.
def brute_force_slow():
    with open('input') as data:
        maximums = []

        for line in tqdm(data.readlines(), desc='Processing input lines'):
            line = line.strip()
            digits = [int(c) for c in line]

            maximum = 0

            # all 12 loops
            for i, d1 in enumerate(digits):
                for j, d2 in enumerate(digits[i+1:]):
                    for k, d3 in enumerate(digits[i+j+2:]):
                        for l, d4 in enumerate(digits[i+j+k+3:]):
                            for m, d5 in enumerate(digits[i+j+k+l+4:]):
                                for n, d6 in enumerate(digits[i+j+k+l+m+5:]):
                                    for o, d7 in enumerate(digits[i+j+k+l+m+n+6:]):
                                        for p, d8 in enumerate(digits[i+j+k+l+m+n+o+7:]):
                                            for q, d9 in enumerate(digits[i+j+k+l+m+n+o+p+8:]):
                                                for r, d10 in enumerate(digits[i+j+k+l+m+n+o+p+q+9:]):
                                                    for s, d11 in enumerate(digits[i+j+k+l+m+n+o+p+q+r+10:]):
                                                        for t, d12 in enumerate(digits[i+j+k+l+m+n+o+p+q+r+s+11:]):
                                                            candidate = d1 * 10**11 + \
                                                                        d2 * 10**10 + \
                                                                        d3 * 10**9 + \
                                                                        d4 * 10**8 + \
                                                                        d5 * 10**7 + \
                                                                        d6 * 10**6 + \
                                                                        d7 * 10**5 + \
                                                                        d8 * 10**4 + \
                                                                        d9 * 10**3 + \
                                                                       d10 * 10**2 + \
                                                                       d11 * 10**1 + \
                                                                       d12 * 10**0
                                                            if candidate > maximum:
                                                                maximum = candidate
            maximums.append(maximum)

        print(f'{sum(maximums)=}')

if __name__ == '__main__':
    with open('input') as data:
        maximums = []
        lines = data.readlines()

        # subsequence search, find max digit with at least 11 digits
        # remaining after it, and so on
        for line in tqdm(lines, desc='Processing input lines'):
            line = line.strip()
            digits = [int(c) for c in line]
            start = 0

            maxdigits = []
            for i in range(12):
                end = len(line) - (11 - i)

                maxdigit = 0
                for j in range(start, end):
                    if digits[j] > maxdigit:
                        maxdigit = digits[j]
                        start = j + 1

                maxdigits.append(maxdigit)

            maximum = 0
            for i, d in enumerate(maxdigits):
                maximum += d * 10**(11-i)

            maximums.append(maximum)

        print(f'{sum(maximums)=}')
