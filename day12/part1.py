#!/usr/bin/env python3

# Thanks Gemini
def rotate(shape):
    transposed = list(map(list, zip(*shape)))
    rotated_shape = [row[::-1] for row in transposed]
    return rotated_shape

if __name__ == '__main__':
    with open('sample') as data:
        shapes = []
        regions = []
        shape = ''

        for line in data:
            if 'x' in line:
                line = line.split(':')
                w, h, = line[0].split('x')
                counts = tuple(int(num) for num in line[1].split())
                regions.append((w, h, counts))
                continue
            
            if ':' in line:
                if shape:
                    shape = [[c for c in l] for l in shape.split()]
                    shapes.append(shape)
                    shape = ''
                continue

            if line:
                shape += line

        print(shapes)
        print(regions)

        print(rotate(shapes[0]))
