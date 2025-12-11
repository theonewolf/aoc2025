#!/usr/bin/env python3

from collections import defaultdict, deque
from functools import cache

nodes = defaultdict(set)

@cache
def dfs(node, dac, fft):
    if node == 'out' and dac and fft:
        return 1

    if node == 'dac':
        dac = True

    if node == 'fft':
        fft = True

    total = 0
    for neighbor in nodes[node]:
        total += dfs(neighbor, dac, fft)

    return total

if __name__ == '__main__':
    # bfs and count the times we hit out?
    with open('input') as data:
        for line in data:
            line = line.strip()
            src, destinations = line.split(':')
            for d in destinations.split():
                nodes[src].add(d)
        
        print(f'{dfs("svr", False, False)}')
