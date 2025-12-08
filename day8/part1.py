#!/usr/bin/env python3

from collections import defaultdict, deque
from heapq import heapify, heappop
from math import sqrt

if __name__ == '__main__':

    def distance(p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        return sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

    with open('input') as data:
        points = []
        for line in data:
            line = line.strip()
            if not line: continue

            line = line.split(',')
            x, y, z = line
            points.append((int(x), int(y), int(z)))

        # 1000 times
        # check for min distance without existing in adjacency matrix
        # we can do O(N**2), priority queue this, and pop point pairs out
        # if in adjacency matrix, don't add again

        # Use repeated BFS to count nodes in the connected sub graphs


        adjacency_list = defaultdict(list)
        min_distances = []

        visited = set()
        for point1 in points:
            for point2 in points:
                if point1 == point2: continue
                if (point1, point2) in visited or (point2, point1) in visited: continue

                min_distances.append((distance(point1, point2), (point1, point2)))
                visited.add((point1, point2))

        heapify(min_distances)

        count = 1000
        while count > 0:
            dist, link = heappop(min_distances)
            p1, p2 = link

            print(f'{dist=} {link=}')

            if p1 not in adjacency_list or p2 not in adjacency_list[p1]:
                adjacency_list[p1].append(p2)
                adjacency_list[p2].append(p1)
                count -= 1

        counts = []
        while points:
            # run BFS, count
            # remove as we walk from adjacency list
            root = points.pop()
            visited = {root}

            queue = deque([root])

            count = 0
            while queue:
                current_node = queue.popleft()
                count += 1

                for neighbor in adjacency_list[current_node]:
                    if neighbor not in visited:
                        points.remove(neighbor)
                        visited.add(neighbor)
                        queue.append(neighbor)

            counts.append(count)


        c1, c2, c3 = sorted(counts, reverse=True)[:3]
        print(c1 * c2 * c3)
