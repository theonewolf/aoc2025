#!/usr/bin/env python3

# merge all overlapping regions
#   sort all ranges
#   for each range
#       if end is inside the next range, then expand
#       else
#           add diff to count

if __name__ == '__main__':
    with open('input') as data:
        fresh = []
        count = 0

        for line in data:
            if not line.strip():
                continue

            elif '-' in line:
                start, end = line.split('-')
                start, end = int(start), int(end)
                fresh.append((start, end))

        fresh = sorted(fresh)

        merged = True
        while merged:
            merged = False
            for i in range(len(fresh)):
                start1, end1 = fresh[i]
                if i < len(fresh) - 1:
                    start2, end2 = fresh[i + 1]
                    if start2 <= end1:
                        # Gemini pointed out I should have used `max` here
                        # I originally just set my end to end2, forgetting that
                        # end2 might accidentally be inside / smaller than end1
                        fresh[i] = (start1, max(end1, end2))

                        # dumb way to delete a range
                        del fresh[i + 1]
                        merged = True
                        break

        for start, end in fresh:
            count += (end - start) + 1

        print(f'{count=}')
