#!/usr/bin/env python3

if __name__ == '__main__':
    with open('input') as data:
        red_tiles = []
        for line in data:
            line = line.strip()
            x, y = line.split(',')
            x, y = int(x), int(y)
            red_tiles.append((x, y))

        maxarea = 0
        for x1, y1 in red_tiles:
            for x2, y2 in red_tiles:
                #print(f'{x1=} {y1=} {x2=} {y2=}')
                l = abs(x1 - x2) + 1
                h = abs(y1 - y2) + 1
                #print(f'\t{l*h=}')

                maxarea = max(maxarea, l * h)

        print(f'{maxarea=}')
