# Game dimensions
CENTER_SIZE = 10  # Size of the central grid where mirrors can be placed
TOTAL_SIZE = CENTER_SIZE + 4  # Total grid size with outer/inner rings
LAST = TOTAL_SIZE - 1  # Index of the last row/column

# Display settings
CELL_SIZE = 50  # Size of each grid cell in pixels
WINDOW_WIDTH = TOTAL_SIZE * CELL_SIZE
WINDOW_HEIGHT = TOTAL_SIZE * CELL_SIZE + 50  # Extra height for buttons

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Mirror types
MIRROR_FORWARD = "/"  # Forward slash
MIRROR_BACKWARD = "\\"  # Backward slash

# Initial fixed numbers on the edges
FIXED_NUMBERS = {
    "top": {4: 112, 6: 48, 7: 3087, 8: 9, 11: 1},
    "left": {5: 27, 9: 12, 10: 225},
    "right": {3: 4, 4: 27, 8: 16},
    "bottom": {2: 2025, 5: 12, 6: 64, 7: 5, 9: 405}
}