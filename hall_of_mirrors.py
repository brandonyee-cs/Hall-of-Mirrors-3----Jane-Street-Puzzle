import pygame
import sys
from game_state import GameState
from renderer import Renderer
from constants import *

def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Hall of Mirror 3 Solver")
    
    # Create the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    # Create game state and renderer
    game_state = GameState()
    renderer = Renderer(screen, game_state)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse input
                if event.button in (1, 3):  # Left or right click
                    x, y = event.pos
                    grid_col = x // CELL_SIZE
                    grid_row = y // CELL_SIZE
                    
                    # Check if click is within playable area (center grid)
                    if (2 <= grid_row < TOTAL_SIZE - 2 and 
                        2 <= grid_col < TOTAL_SIZE - 2):
                        mirror_row = grid_row - 2
                        mirror_col = grid_col - 2
                        game_state.toggle_mirror(mirror_row, mirror_col, event.button)
            
            # Handle toggle buttons for showing/hiding lines
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x, y = event.pos
                if 10 <= y <= 40:  # Button row
                    if 10 <= x <= 160:  # Green toggle button
                        game_state.toggle_show_green()
                    elif 170 <= x <= 320:  # Red toggle button
                        game_state.toggle_show_red()
        
        # Draw everything
        screen.fill(WHITE)
        renderer.draw()
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()