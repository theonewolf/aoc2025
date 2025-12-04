#!/usr/bin/env python3

def sumrolls(row, col, grid):
    directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    max_row = len(grid)
    max_col = len(grid[0])

    count = 0
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if (new_row >= 0 and new_row < max_row) and (new_col >= 0 and new_col < max_col):
            #print(f'checking {new_row=} {new_col=} got {grid[new_row][new_col]=}')
            if grid[new_row][new_col] == '@':
                count += 1

    return count

if __name__ == '__main__':
    with open('input') as data:
        grid = [list(l.strip()) for l in data.readlines()]

        total = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == '@':
                    if sumrolls(row, col, grid) < 4:
                        total += 1

        #for row in grid:
        #    print(''.join(row))

        print(f'{total=}')

