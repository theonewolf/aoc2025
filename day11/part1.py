#!/usr/bin/env python3

from collections import defaultdict, deque

if __name__ == '__main__':
    # bfs and count the times we hit out?
    with open('input') as data:
        nodes = defaultdict(list)
        for line in data:
            line = line.strip()
            src, destinations = line.split(':')
            for d in destinations.split():
                nodes[src].append(d)


        queue = deque(['you'])
        visited = set(['you'])

        count = 0
        while queue:
            node = queue.popleft()

            if node == 'out':
                count += 1

            for neighbor in nodes[node]:
                queue.append(neighbor)

        print(f'{count=}')
