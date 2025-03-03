# Hall of Mirrors 3 Solver

A Python Puzzle Solver for Jane Street Puzzle Hall of Mirrors 3.

## Description

This is a simulator for a grid-based puzzle where lasers are shot from the edges of the grid, reflect off mirrors placed in the center grid, and exit at other edges. The goal is to place mirrors correctly to make the path products match the target values on the grid edges.

## Features

- Interactive grid where you can place and remove mirrors
- Lasers shoot from edges and reflect off mirrors
- Path products are calculated and displayed
- Color-coded paths (green for correct, red for incorrect)
- Toggle buttons to show/hide green or red paths

## Controls

- **Left-click** on a grid cell to place or remove a forward slash (/) mirror
- **Right-click** on a grid cell to place or remove a backslash (\\) mirror
- Click the toggle buttons at the top to show/hide green or red paths

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required packages:

```
pip install -r requirements.txt
```

3. Run the game:

```
python hall_of_mirrors.py
```

## Project Structure

- `hall_of_mirrors.py` - Main entry point
- `game_state.py` - Game state and logic
- `renderer.py` - Pygame rendering
- `constants.py` - Game constants and configuration

## How Laser Path Products Work

1. A laser starts from an edge cell and travels in a straight line
2. Each line segment counts steps until it hits a mirror or exits
3. When a laser hits a mirror, it reflects and starts a new segment
4. The product of all segment step counts is the final result
5. The goal is to match this product with the target number

The target numbers are fixed on the grid edges, and resulting products are shown in parentheses. Green indicates a match, red indicates a mismatch.