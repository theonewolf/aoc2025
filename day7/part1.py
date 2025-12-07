#!/usr/bin/env python3

from copy import deepcopy
from pprint import pprint

if __name__ == '__main__':
    with open('input') as data:
        grid = []
        for line in data:
            grid.append(list(line.strip()))

        beamsplit = 0
        modified = True
        while modified:
            modified = False
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if row + 1 >= len(grid):
                        continue
                    match grid[row][col]:
                        case 'S':
                            if grid[row + 1][col] != '|' and grid[row + 1][col] == '.':
                                grid[row + 1][col] = '|'
                                modified = True
                        case '|':
                            if grid[row + 1][col] != '|' and grid[row + 1][col] == '.':
                                modified = True
                                grid[row + 1][col] = '|'
                        case '^':
                            if grid[row - 1][col] == '|':
                                if grid[row][col - 1] != '|' or grid[row][col + 1] != '|':
                                    grid[row][col - 1] = '|' 
                                    grid[row][col + 1] = '|'
                                    modified = True

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                match grid[row][col]:
                    case '^':
                        if grid[row - 1][col] == '|':
                            beamsplit += 1

        pprint([''.join(row) for row in grid])
        print(f'{beamsplit=}')
