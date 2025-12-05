#!/usr/bin/env python3

if __name__ == '__main__':
    with open('input') as data:
        fresh = []
        count = 0

        for line in data:
            if not line.strip():
                continue

            elif '-' in line:
                start, end = line.split('-')
                start, end = int(start), int(end)
                fresh.append((start, end))

            else:
                ingredient = int(line)
                for start, end in fresh:
                    if start <= ingredient <= end:
                        count += 1
                        break

        print(f'{count=}')
