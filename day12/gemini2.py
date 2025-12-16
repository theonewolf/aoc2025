#!/usr/bin/env python3
import sys
from ortools.sat.python import cp_model
import copy
import time # Added for timing the solver

import signal # NEW: Import the signal module

def signal_handler(signum, frame):
    """Handles Ctrl+C signal for immediate termination."""
    print("\n\n🛑 Program received interrupt signal (Ctrl+C). Terminating execution.")
    # If the solver is running, setting a time limit to 0 helps it stop quickly.
    # However, for a clean exit, sys.exit() is often necessary here.
    sys.exit(0)

# Install the signal handler immediately
signal.signal(signal.SIGINT, signal_handler)

# --- Helper Functions ---

def rotate_90_clockwise(shape):
    """Rotates a 2D shape 90 degrees clockwise."""
    transposed = list(map(list, zip(*shape)))
    rotated_shape = [row[::-1] for row in transposed] 
    return rotated_shape

def print_region(region, width, height):
    """Prints the final region grid."""
    print(f"\n--- Region {width}x{height} ---")
    if region:
        for row in region:
            print(''.join(row))
    print("----------------------------")

def place_shape(region, shape, r, c, shape_id):
    """
    Places the shape onto the region grid at (r, c).
    Note: r corresponds to Y (row index), c corresponds to X (column index).
    """
    s_rows = len(shape)
    s_cols = len(shape[0])

    for i in range(s_rows):
        for j in range(s_cols):
            # Only place if the shape cell is filled (not '.')
            if shape[i][j] != '.':
                region[r + i][c + j] = shape_id
    
    return region

def pre_process_shapes(shapes):
    """
    Generates all unique orientations and their bounding box dimensions.
    Returns: (all_orient_dims, all_orient_grids)
    """
    all_orient_dims = []
    all_orient_grids = []
    
    for shape_idx, original_shape in enumerate(shapes):
        orient_dims = []
        orient_grids = []
        current_shape = original_shape
        
        # Loop up to 4 times for 0, 90, 180, 270 degrees
        for _ in range(4):
            rows = len(current_shape)
            cols = len(current_shape[0]) if rows > 0 else 0
            dims = (rows, cols)
            
            # Check for uniqueness using the grid content
            hashable_grid = tuple(tuple(row) for row in current_shape)
            if hashable_grid not in [tuple(tuple(r) for r in g) for g in orient_grids]:
                orient_dims.append(dims)
                orient_grids.append(copy.deepcopy(current_shape)) 

            current_shape = rotate_90_clockwise(current_shape)

        all_orient_dims.append(orient_dims)
        all_orient_grids.append(orient_grids)
        
    return all_orient_dims, all_orient_grids

# --- CP-SAT Core Solver (FIXED) ---

def solve_region_with_cp_sat(shapes, region_def):
    """
    Solves the 2D packing problem using CP-SAT with Bounding Box non-overlap.
    """
    try:
        W = int(region_def[0]) # Width (X axis)
        H = int(region_def[1]) # Height (Y axis)
        shape_counts = region_def[2]
    except ValueError:
        print("Error: Invalid region dimensions or counts.")
        return None, False

    # Pre-process shapes to get all rotations and dimensions
    all_orient_dims, all_orient_grids = pre_process_shapes(shapes)

    model = cp_model.CpModel()
    
    # --- 1. Map all required pieces to a unique ID ---
    all_pieces = [] 
    piece_index_to_shape_idx = {}
    global_piece_id = 0
    
    for shape_idx, count in enumerate(shape_counts):
        for _ in range(count):
            piece_index_to_shape_idx[global_piece_id] = shape_idx
            all_pieces.append(global_piece_id)
            global_piece_id += 1
            
    print(f"\nAttempting to solve Region {W}x{H} with CP-SAT (Total pieces: {len(all_pieces)})")

    # --- 2. Define Variables and Constraints ---
    
    piece_x = {}
    piece_y = {}
    piece_w = {}
    piece_h = {}
    piece_x_end = {}  # NEW: End X variable
    piece_y_end = {}  # NEW: End Y variable
    piece_r = {} 
    
    x_intervals = [] 
    y_intervals = [] 
    
    for i in all_pieces:
        shape_idx = piece_index_to_shape_idx[i]
        orientations_count = len(all_orient_dims[shape_idx])
        max_dim = max(max(r, c) for r, c in all_orient_dims[shape_idx])

        # Placement Coordinates (Bottom-Left Corner)
        piece_x[i] = model.NewIntVar(0, W - 1, f'x_{i}')
        piece_y[i] = model.NewIntVar(0, H - 1, f'y_{i}')
        
        # Dimensions
        piece_w[i] = model.NewIntVar(1, max_dim, f'w_{i}')
        piece_h[i] = model.NewIntVar(1, max_dim, f'h_{i}')
        
        # Orientation choice: Only one must be true
        piece_r[i] = [model.NewBoolVar(f'r_{i}_{j}') for j in range(orientations_count)]
        model.AddExactlyOne(piece_r[i])

        # Link Orientation to Dimensions and Boundaries
        for j in range(orientations_count):
            rows, cols = all_orient_dims[shape_idx][j]
            
            # If orientation j is chosen (piece_r[i][j] == 1):
            model.Add(piece_w[i] == cols).OnlyEnforceIf(piece_r[i][j])
            model.Add(piece_h[i] == rows).OnlyEnforceIf(piece_r[i][j])
            model.Add(piece_x[i] + cols <= W).OnlyEnforceIf(piece_r[i][j])
            model.Add(piece_y[i] + rows <= H).OnlyEnforceIf(piece_r[i][j])
            
        # FIX: Define the END coordinates explicitly and link them
        piece_x_end[i] = model.NewIntVar(1, W, f'x_end_{i}')
        piece_y_end[i] = model.NewIntVar(1, H, f'y_end_{i}')
        
        # FIX: Link start, size, and end: start + size = end
        # This resolves the TypeError by ensuring 'end' is a variable itself.
        model.Add(piece_x_end[i] == piece_x[i] + piece_w[i])
        model.Add(piece_y_end[i] == piece_y[i] + piece_h[i])

        # Create Interval variables using the explicit start, size, and end variables
        x_intervals.append(
            model.NewIntervalVar(
                piece_x[i],      # start
                piece_w[i],      # size
                piece_x_end[i],  # end 
                f'x_interval_{i}'
            )
        )
        y_intervals.append(
            model.NewIntervalVar(
                piece_y[i],      # start
                piece_h[i],      # size
                piece_y_end[i],  # end
                f'y_interval_{i}'
            )
        )
        

    # --- 3. Non-Overlap Constraint (Bounding Box) ---
    model.AddNoOverlap2D(x_intervals, y_intervals)
    
    # --- 4. Solve and Extract Result ---
    
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = False
	
	# --- ADD THESE PARAMETERS ---
    # Limit the solver to a maximum of 60 seconds (adjust as needed)
    solver.parameters.max_time_in_seconds = 120
    
    start_time = time.time()
    status = solver.Solve(model)
    end_time = time.time()
    
    print(f"  Solver finished in {end_time - start_time:.3f} seconds.")

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("  Solution found!")
        
        # Reconstruct the grid
        final_region = [['.' for _ in range(W)] for _ in range(H)]
        
        for i in all_pieces:
            x_val = solver.Value(piece_x[i])
            y_val = solver.Value(piece_y[i])
            shape_idx = piece_index_to_shape_idx[i]
            
            # Find the chosen orientation index (j)
            chosen_orientation = -1
            for j in range(len(piece_r[i])):
                if solver.Value(piece_r[i][j]):
                    chosen_orientation = j
                    break
            
            placed_shape = all_orient_grids[shape_idx][chosen_orientation]
            shape_id = chr(ord('A') + shape_idx)

            # Place the non-rectangular shape onto the grid
            final_region = place_shape(final_region, placed_shape, y_val, x_val, shape_id)

        return final_region, True
    
    else:
        print("  Solution NOT found. Region is un-packable (under bounding box constraints).")
        return None, False

# ----------------------------------------------------------------------
# Execution Block
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
50x45: 0 0 0 0 0 240
"""
    sample_data_string = open('input').read()
    
    # Added the large region 50x45 with 240 pieces of shape 5 (3x3) which likely caused the timeout/type error.

    shapes_loaded = []
    regions_loaded = []
    
    # Custom parsing function for the given format
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

    # ----------------------------------------------------------------------
    # Execution: Solve all loaded regions using CP-SAT
    # ----------------------------------------------------------------------
    successful_regions_count = 0

    try:
        for i, region_def in enumerate(regions_loaded):
            final_region, success = solve_region_with_cp_sat(shapes_loaded, region_def)
            
            if final_region:
                W, H = region_def[0], region_def[1]
                status = "SUCCESS" if success else "FAILURE"
                print(f"\n-- Results for Region {i + 1} ({W}x{H}) - {status} --")
                print_region(final_region, W, H)

                if success:
                    successful_regions_count += 1
    except KeyboardInterrupt:
        # Catch the Ctrl+C signal
        print("\n\n🛑 Program interrupted by user (Ctrl+C). Terminating execution.")
        
        # Print a summary of work completed up to the interruption
        print("--- Interruption Summary ---")
        print(f"Regions successfully packed before interruption: {successful_regions_count}")
        print(f"Total regions attempted: {i + 1}")
        
        # Crucial step: Exit the entire script cleanly
        sys.exit(0)
                
    print("\n" + "="*60)
    print(f"📊 Summary: {successful_regions_count} / {len(regions_loaded)} regions successfully packed.")
    print("NOTE: Success is based on Bounding Box Non-Overlap.")
    print("="*60)
