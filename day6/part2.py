#!/usr/bin/env python3

def column_positions(grid):
    cols = []
    for col in range(len(grid[0])):
        column = ''.join([grid[row][col] for row in range(len(grid))]).strip()
        if not column:
            cols.append(col)

    return cols

def col_to_num(column):
    print(f'{column=}')
    grid = []

    for row in column:
        grid.append(row)

    maxlen = max([len(row) for row in grid])

    for i, row in enumerate(grid):
        while len(row) < maxlen:
            row += ' '
        grid[i] = row
    
    numbers = []
    for i in range(maxlen):
        numbers.append(int(''.join([grid[r][i] for r in range(len(grid) - 1)])))

    print(f'\t{numbers=}')

    operator = grid[-1].strip()

    accumulator = None
    match operator:
        case '+':
            accumulator = 0
        case '*':
            accumulator = 1

    for number in numbers:
        match operator:
            case '+':
                accumulator += number
            case '*':
                accumulator *= number

    return accumulator

if __name__ == '__main__':
    with open('input') as data:
        newdata = []
        for line in data:
            newdata.append(line)

        columns_pos_list = column_positions(newdata)

        columns = []
        col_start = 0
        for col_end in columns_pos_list:
            column = []
            for row in newdata:
                column.append(row[col_start:col_end])
            columns.append(column)
            col_start = col_end + 1

        print(columns)
        results = []
        for col in columns:
            results.append(col_to_num(col))

        print(f'{sum(results)=}')
