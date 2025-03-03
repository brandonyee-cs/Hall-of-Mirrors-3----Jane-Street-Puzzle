import pygame
from game_state import GameState
from constants import *

class Renderer:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.SysFont('Arial', 16)
        self.button_font = pygame.font.SysFont('Arial', 14)
    
    def draw(self):
        """Main drawing function"""
        # Draw toggle buttons
        self.draw_buttons()
        
        # Draw grid cells and contents
        self.draw_grid()
        
        # Draw laser paths
        self.draw_laser_paths()
    
    def draw_buttons(self):
        """Draw the toggle buttons for green/red lines"""
        # Green toggle button
        button_color = GREEN if self.game_state.show_green else GRAY
        pygame.draw.rect(self.screen, button_color, (10, 10, 150, 30))
        text = "Hide Green Lines" if self.game_state.show_green else "Show Green Lines"
        text_surf = self.button_font.render(text, True, BLACK)
        self.screen.blit(text_surf, (20, 15))
        
        # Red toggle button
        button_color = RED if self.game_state.show_red else GRAY
        pygame.draw.rect(self.screen, button_color, (170, 10, 150, 30))
        text = "Hide Red Lines" if self.game_state.show_red else "Show Red Lines"
        text_surf = self.button_font.render(text, True, BLACK)
        self.screen.blit(text_surf, (180, 15))
    
    def draw_grid(self):
        """Draw the grid cells and their contents"""
        # Top offset for grid (after buttons)
        offset_y = 50
        
        for row in range(TOTAL_SIZE):
            for col in range(TOTAL_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE + offset_y
                
                # Draw cell boundary
                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                
                # Outer ring cells - show fixed numbers and laser outputs
                if row == 0 or row == LAST or col == 0 or col == LAST:
                    self.draw_outer_cell(row, col, x, y)
                
                # Inner ring cells - show dots
                elif (row == 1 or row == LAST-1 or col == 1 or col == LAST-1) and not (
                    (row == 1 and col == 1) or 
                    (row == 1 and col == LAST-1) or
                    (row == LAST-1 and col == 1) or
                    (row == LAST-1 and col == LAST-1)
                ):
                    # Draw a dot
                    pygame.draw.circle(self.screen, BLACK, (x + CELL_SIZE//2, y + CELL_SIZE//2), 3)
                
                # Center cells - show mirrors
                elif 2 <= row < TOTAL_SIZE-2 and 2 <= col < TOTAL_SIZE-2:
                    mirror_row, mirror_col = row-2, col-2
                    mirror_type = self.game_state.mirrors.get((mirror_row, mirror_col))
                    
                    if mirror_type:
                        if mirror_type == MIRROR_FORWARD:  # /
                            pygame.draw.line(self.screen, BLACK, 
                                            (x + 5, y + CELL_SIZE - 5), 
                                            (x + CELL_SIZE - 5, y + 5), 2)
                        else:  # mirror_type == MIRROR_BACKWARD (\)
                            pygame.draw.line(self.screen, BLACK,
                                            (x + 5, y + 5),
                                            (x + CELL_SIZE - 5, y + CELL_SIZE - 5), 2)
    
    def draw_outer_cell(self, row, col, x, y):
        """Draw the contents of outer ring cells"""
        # Check if this cell has a fixed number (target value)
        fixed_num = None
        if row == 0 and col in self.game_state.fixed_numbers["top"]:
            fixed_num = self.game_state.fixed_numbers["top"][col]
        elif row == LAST and col in self.game_state.fixed_numbers["bottom"]:
            fixed_num = self.game_state.fixed_numbers["bottom"][col]
        elif col == 0 and row in self.game_state.fixed_numbers["left"]:
            fixed_num = self.game_state.fixed_numbers["left"][row]
        elif col == LAST and row in self.game_state.fixed_numbers["right"]:
            fixed_num = self.game_state.fixed_numbers["right"][row]
        
        # Draw fixed number
        if fixed_num is not None:
            text_surf = self.font.render(str(fixed_num), True, BLACK)
            text_rect = text_surf.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
            self.screen.blit(text_surf, text_rect)
        
        # Draw laser output if it exists for this cell
        output = self.game_state.laser_outputs.get((row, col))
        if output:
            color = GREEN if output.color == "green" else RED
            output_text = f"({output.product})"
            text_surf = self.font.render(output_text, True, color)
            
            # Position the text to the right if there's a fixed number
            if fixed_num is not None:
                text_rect = text_surf.get_rect(midleft=(x + CELL_SIZE//2 + 5, y + CELL_SIZE//2))
            else:
                text_rect = text_surf.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
            
            self.screen.blit(text_surf, text_rect)
    
    def draw_laser_paths(self):
        """Draw the laser path lines"""
        offset_y = 50  # Same offset as in draw_grid
        
        for segment in self.game_state.laser_segments:
            # Skip if we're not showing this color
            if segment.color == "green" and not self.game_state.show_green:
                continue
            if segment.color == "red" and not self.game_state.show_red:
                continue
            
            # Convert grid coordinates to pixel coordinates
            start_x = segment.start[1] * CELL_SIZE + CELL_SIZE // 2
            start_y = segment.start[0] * CELL_SIZE + CELL_SIZE // 2 + offset_y
            end_x = segment.end[1] * CELL_SIZE + CELL_SIZE // 2
            end_y = segment.end[0] * CELL_SIZE + CELL_SIZE // 2 + offset_y
            
            # Determine color
            color = GREEN if segment.color == "green" else RED
            
            # Draw the line
            pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), 2)