from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
from constants import *

@dataclass
class LineSegment:
    """A line segment in the grid representing part of a laser path"""
    start: Tuple[int, int]  # (row, col) start coordinates
    end: Tuple[int, int]    # (row, col) end coordinates
    color: str = None       # "green" or "red"

@dataclass
class LaserOutput:
    """Result of a laser path calculation"""
    product: int
    color: str  # "green" or "red"

class GameState:
    def __init__(self):
        # Fixed numbers on the grid edges (targets)
        self.fixed_numbers = FIXED_NUMBERS
        
        # Mirror positions {(row, col): mirror_type}
        self.mirrors = {}
        
        # Line segments for laser paths
        self.laser_segments = []
        
        # Store the final outputs for each laser
        self.laser_outputs = {}
        
        # Visibility toggles
        self.show_green = True
        self.show_red = True
        
        # Calculate initial laser paths
        self.calculate_laser_paths()
    
    def toggle_mirror(self, row: int, col: int, button: int):
        """Toggle mirror at the given position based on mouse button"""
        key = (row, col)
        
        if button == 1:  # Left click - toggle forward slash
            if self.mirrors.get(key) == MIRROR_FORWARD:
                del self.mirrors[key]
            else:
                self.mirrors[key] = MIRROR_FORWARD
        elif button == 3:  # Right click - toggle backslash
            if self.mirrors.get(key) == MIRROR_BACKWARD:
                del self.mirrors[key]
            else:
                self.mirrors[key] = MIRROR_BACKWARD
        
        # Recalculate laser paths
        self.calculate_laser_paths()
    
    def toggle_show_green(self):
        """Toggle visibility of green laser paths"""
        self.show_green = not self.show_green
    
    def toggle_show_red(self):
        """Toggle visibility of red laser paths"""
        self.show_red = not self.show_red
    
    def calculate_laser_paths(self):
        """Calculate all laser paths and their outcomes"""
        self.laser_segments = []
        self.laser_outputs = {}
        
        # Process lasers from top
        for col, target in self.fixed_numbers["top"].items():
            result = self.shoot_laser(1, col, 1, 0)  # Down direction
            color = "green" if result["product"] == target else "red"
            
            # Color all segments
            for segment in result["segments"]:
                segment.color = color
                self.laser_segments.append(segment)
            
            # Store the output
            out_pos = self.outer_cell_for_dot(*result["final_dot"])
            if 0 <= out_pos[0] <= LAST and 0 <= out_pos[1] <= LAST:
                self.laser_outputs[out_pos] = LaserOutput(result["product"], color)
        
        # Process lasers from bottom
        for col, target in self.fixed_numbers["bottom"].items():
            result = self.shoot_laser(LAST-1, col, -1, 0)  # Up direction
            color = "green" if result["product"] == target else "red"
            
            # Color all segments
            for segment in result["segments"]:
                segment.color = color
                self.laser_segments.append(segment)
            
            # Store the output
            out_pos = self.outer_cell_for_dot(*result["final_dot"])
            if 0 <= out_pos[0] <= LAST and 0 <= out_pos[1] <= LAST:
                self.laser_outputs[out_pos] = LaserOutput(result["product"], color)
        
        # Process lasers from left
        for row, target in self.fixed_numbers["left"].items():
            result = self.shoot_laser(row, 1, 0, 1)  # Right direction
            color = "green" if result["product"] == target else "red"
            
            # Color all segments
            for segment in result["segments"]:
                segment.color = color
                self.laser_segments.append(segment)
            
            # Store the output
            out_pos = self.outer_cell_for_dot(*result["final_dot"])
            if 0 <= out_pos[0] <= LAST and 0 <= out_pos[1] <= LAST:
                self.laser_outputs[out_pos] = LaserOutput(result["product"], color)
        
        # Process lasers from right
        for row, target in self.fixed_numbers["right"].items():
            result = self.shoot_laser(row, LAST-1, 0, -1)  # Left direction
            color = "green" if result["product"] == target else "red"
            
            # Color all segments
            for segment in result["segments"]:
                segment.color = color
                self.laser_segments.append(segment)
            
            # Store the output
            out_pos = self.outer_cell_for_dot(*result["final_dot"])
            if 0 <= out_pos[0] <= LAST and 0 <= out_pos[1] <= LAST:
                self.laser_outputs[out_pos] = LaserOutput(result["product"], color)
    
    def reflect_direction(self, dx: int, dy: int, mirror_type: str) -> Tuple[int, int]:
        """Calculate the new direction after reflection"""
        if mirror_type == MIRROR_FORWARD:  # /
            if dx == -1 and dy == 0: return (0, -1)  # up -> left
            if dx == 1 and dy == 0: return (0, 1)    # down -> right
            if dx == 0 and dy == -1: return (-1, 0)  # left -> up
            if dx == 0 and dy == 1: return (1, 0)    # right -> down
        else:  # mirror_type == MIRROR_BACKWARD (\)
            if dx == -1 and dy == 0: return (0, 1)   # up -> right
            if dx == 1 and dy == 0: return (0, -1)   # down -> left
            if dx == 0 and dy == -1: return (1, 0)   # left -> down
            if dx == 0 and dy == 1: return (-1, 0)   # right -> up
        
        # Fallback (should not reach here)
        return (dx, dy)
    
    def shoot_laser(self, start_row: int, start_col: int, dx: int, dy: int) -> Dict:
        """Simulate a laser shooting from start position in the given direction"""
        row, col = start_row, start_col
        segments = []
        product = 1
        
        seg_start = (row, col)
        steps = 0
        
        while True:
            row += dx
            col += dy
            steps += 1
            
            # Check if out of bounds
            if row < 0 or row > LAST or col < 0 or col > LAST:
                segments.append(LineSegment(seg_start, (row, col)))
                product *= steps
                return {
                    "segments": segments,
                    "product": product,
                    "final_dot": (row, col)
                }
            
            # Check if we hit an inner ring dot (that's not our starting point)
            if ((row == 1 or row == LAST-1 or col == 1 or col == LAST-1) and
                (row != start_row or col != start_col)):
                segments.append(LineSegment(seg_start, (row, col)))
                product *= steps
                return {
                    "segments": segments,
                    "product": product,
                    "final_dot": (row, col)
                }
            
            # Check if we hit a mirror in the center area
            if 2 <= row <= LAST-2 and 2 <= col <= LAST-2:
                mirror_key = (row-2, col-2)
                if mirror_key in self.mirrors:
                    mirror_type = self.mirrors[mirror_key]
                    
                    # End current segment
                    segments.append(LineSegment(seg_start, (row, col)))
                    product *= steps
                    
                    # Calculate new direction after reflection
                    dx, dy = self.reflect_direction(dx, dy, mirror_type)
                    
                    # Start new segment
                    seg_start = (row, col)
                    steps = 0
    
    def outer_cell_for_dot(self, row: int, col: int) -> Tuple[int, int]:
        """Convert an inner ring dot position to the corresponding outer cell position"""
        if row == 1: return (0, col)           # Top edge
        if row == LAST-1: return (LAST, col)   # Bottom edge
        if col == 1: return (row, 0)           # Left edge
        if col == LAST-1: return (row, LAST)   # Right edge
        return (row, col)  # Fallback