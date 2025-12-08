#!/usr/bin/env python3

from collections import defaultdict, deque
from copy import deepcopy
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

        counts = [0]
        while max(counts) != len(points):
            min_distances_copy = deepcopy(min_distances)

            lastp1, lastp2 = None, None
            # Manually did binary search to find 7224
            for i in range(7224):
                dist, link = heappop(min_distances_copy)
                p1, p2 = link
                lastp1, lastp2 = p1, p2

                if p1 not in adjacency_list or p2 not in adjacency_list[p1]:
                    adjacency_list[p1].append(p2)
                    adjacency_list[p2].append(p1)

            print(f'{lastp1} {lastp2}')
            print(f'{lastp1[0] * lastp2[0]}')

            counts = []
            points_copy = deepcopy(points)
            while points_copy:
                # run BFS, count
                # remove as we walk from adjacency list
                root = points_copy.pop()
                visited = {root}

                queue = deque([root])

                count = 0
                while queue:
                    current_node = queue.popleft()
                    count += 1

                    for neighbor in adjacency_list[current_node]:
                        if neighbor not in visited:
                            points_copy.remove(neighbor)
                            visited.add(neighbor)
                            queue.append(neighbor)

                counts.append(count)
            print(f'{max(counts)} / {len(points)}')
