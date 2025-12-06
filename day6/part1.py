#!/usr/bin/env python3

if __name__ == '__main__':
    with open('input') as data:
        newdata = []
        for line in data:
            newdata.append(line.split())

        results = []
        for col in range(len(newdata[0])):
            operator = newdata[-1][col]

            accumulator = None
            match operator:
                case '+':
                    accumulator = 0
                case '*':
                    accumulator = 1

            for row in range(len(newdata) - 1):
                print(f'{col=} {row=} {newdata[row][col]}')
                val = int(newdata[row][col])

                match operator:
                    case '+':
                        accumulator += val
                    case '*':
                        accumulator *= val

            results.append(accumulator)

        print(f'{sum(results)=}')
