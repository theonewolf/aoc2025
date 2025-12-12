#!/usr/bin/env python3

import sys
import copy
import random
import time

# --- Helper Functions (Same as before) ---
def rotate_90_clockwise(shape):
    """Rotates a 2D shape 90 degrees clockwise."""
    transposed = list(map(list, zip(*shape)))
    rotated_shape = [row[::-1] for row in transposed] 
    return rotated_shape

def print_region(region, width, height):
    # ... (same as before)
    print(f"\n--- Region {width}x{height} ---")
    for row in region:
        print(''.join(row))
    print("----------------------------")

def can_place(region, shape, r, c):
    # ... (same as before)
    R = len(region)
    C = len(region[0])
    s_rows = len(shape)
    s_cols = len(shape[0])
    if r + s_rows > R or c + s_cols > C: return False
    for i in range(s_rows):
        for j in range(s_cols):
            if shape[i][j] != '.' and region[r + i][c + j] != '.': return False  
    return True

def place_shape(region, shape, r, c, shape_id):
    # ... (same as before)
    s_rows = len(shape)
    s_cols = len(shape[0])
    for i in range(s_rows):
        for j in range(s_cols):
            if shape[i][j] != '.':
                region[r + i][c + j] = shape_id
    return region


# --- Core Packing Logic (Probabilistic Search) ---

def attempt_random_pack(shapes, region_def, piece_order):
    """
    Attempts to pack shapes into a region following a specific piece order,
    trying orientations in a randomized order.
    
    Args:
        shapes: List of all shape definitions.
        region_def: (W, H, counts)
        piece_order: List of shape_idx (the only thing needed here).
        
    Returns:
        tuple: (The packed region grid, success_boolean)
    """
    W = int(region_def[0])
    H = int(region_def[1])
    # Use a deepcopy of the empty region to start fresh
    region = [['.' for _ in range(W)] for _ in range(H)] 
    
    pieces_placed = 0

    for shape_idx in piece_order:
        original_shape = shapes[shape_idx]
        shape_id = chr(ord('A') + shape_idx) if shape_idx < 26 else str(shape_idx)
        
        # --- Generate all unique 90-degree orientations ---
        orientations = []
        current_shape = original_shape
        
        for _ in range(4):
            hashable_shape = tuple(tuple(row) for row in current_shape)
            if hashable_shape not in [tuple(tuple(r) for r in o) for o in orientations]:
                orientations.append(copy.deepcopy(current_shape)) 
            current_shape = rotate_90_clockwise(current_shape)

        # RANDOMIZATION STEP 2: Shuffle the order of orientations to try
        random.shuffle(orientations)
        
        placed = False
        
        # Greedy Placement: Scan the region from top-left (r=0, c=0)
        for r in range(H):
            for c in range(W):
                
                # Try all unique orientations in RANDOM ORDER
                for shape_to_try in orientations:
                    if can_place(region, shape_to_try, r, c):
                        region = place_shape(region, shape_to_try, r, c, shape_id)
                        pieces_placed += 1
                        placed = True
                        break 
                if placed:
                    break  
            if placed:
                break 

        if not placed:
            # If even one piece can't be placed, this trial fails
            return region, False 
    
    # Success only if all pieces were placed
    return region, pieces_placed == len(piece_order)

def solve_region_probabilistically(shapes, region_def, max_trials=1000):
    """
    Repeats the random packing attempt N times to find a successful solution.
    """
    W, H, shape_counts = region_def
    W, H = int(W), int(H)
    
    # 1. Generate the master list of all pieces required (Indices only)
    all_pieces_indices = [] 
    for shape_idx in range(len(shapes)):
        count_needed = shape_counts[shape_idx]
        for _ in range(count_needed):
            all_pieces_indices.append(shape_idx) 

    
    print(f"\nAttempting to pack a {W}x{H} region with {max_trials} randomized trials...")
    
    best_region = None
    
    for trial in range(1, max_trials + 1):
        # RANDOMIZATION STEP 1: Shuffle the order of pieces
        current_piece_order = all_pieces_indices[:] # Copy the list
        random.shuffle(current_piece_order) 
        
        final_region, success = attempt_random_pack(shapes, region_def, current_piece_order)
        
        if success:
            print(f"  SUCCESS achieved on Trial {trial}/{max_trials}!")
            return final_region, True
        
        # Keep the result of the last trial just in case we need to print a failure
        best_region = final_region
        
        # Print progress update
        if trial % 100 == 0:
            print(f"  ... Trial {trial}/{max_trials} complete.")

    # If the loop finishes without success
    print(f"  Failure: Could not find a solution in {max_trials} trials.")
    return best_region, False

# ----------------------------------------------------------------------
# Execution Block (Uses your specific input data)
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Your sample data
    sample_data_string = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

    sample_data_string=open('input').read()
    
    shapes_loaded = []
    regions_loaded = []
    
    # Custom parsing function for the given format (same as before)
    def parse_sample_data(data):
        current_shape_str = ""
        lines = data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.endswith(':'):
                if current_shape_str:
                    shapes_loaded.append([[c for c in l] for l in current_shape_str.strip().split('\n')])
                    current_shape_str = ""
                continue
            if 'x' in line and ':' in line:
                if current_shape_str:
                    shapes_loaded.append([[c for c in l] for l in current_shape_str.strip().split('\n')])
                    current_shape_str = ""
                parts = line.split(':')
                w, h = parts[0].split('x')
                counts = tuple(int(num) for num in parts[1].split())
                regions_loaded.append((w, h, counts))
                continue
            
            if current_shape_str: current_shape_str += '\n'
            current_shape_str += line
            
        if current_shape_str:
            shapes_loaded.append([[c for c in l] for l in current_shape_str.strip().split('\n')])

    parse_sample_data(sample_data_string)

    print(f"\n✅ Data Loaded. Shapes: {len(shapes_loaded)}, Regions: {len(regions_loaded)}")
    random.seed(42) # Set a seed for consistent results across runs

    # ----------------------------------------------------------------------
    # Execution: Pack all loaded regions and track success
    # ----------------------------------------------------------------------
    successful_regions_count = 0
    MAX_TRIALS = 10 # The N value for the probabilistic search

    for i, region_def in enumerate(regions_loaded):
        # Use the probabilistic solver
        final_region, success = solve_region_probabilistically(shapes_loaded, region_def, max_trials=MAX_TRIALS)
        
        if final_region:
            W, H = region_def[0], region_def[1]
            status = "SUCCESS" if success else "FAILURE"
            print(f"\n-- Results for Region {i + 1} ({W}x{H}) - {status} --")
            print_region(final_region, W, H)

            if success:
                successful_regions_count += 1
                
    print("\n" + "="*40)
    print(f"📊 Summary: {successful_regions_count} / {len(regions_loaded)} regions successfully fit all shapes.")
    print("="*40)
