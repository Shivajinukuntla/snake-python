import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 8
CELL_SIZE = 50
MARGIN = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush Clone")

# Colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
WHITE = (255, 255, 255)

# Create grid
grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to draw the grid
def draw_grid():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[row][col],
                             [(MARGIN + CELL_SIZE) * col + MARGIN,
                              (MARGIN + CELL_SIZE) * row + MARGIN,
                              CELL_SIZE, CELL_SIZE])

def swap_cells(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

def find_matches():
    matches = set()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.update([(row, col), (row, col + 1), (row, col + 2)])
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.update([(row, col), (row + 1, col), (row + 2, col)])
    return matches

def remove_matches():
    matches = find_matches()
    for row, col in matches:
        grid[row][col] = random.choice(COLORS)
    return len(matches) > 0

running = True
clock = pygame.time.Clock()
selected_cell = None

while running:
    draw_grid()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // (CELL_SIZE + MARGIN)
            row = y // (CELL_SIZE + MARGIN)
            if selected_cell:
                if abs(selected_cell[0] - row) + abs(selected_cell[1] - col) == 1:
                    swap_cells(selected_cell, (row, col))
                    if not remove_matches():
                        swap_cells(selected_cell, (row, col))  # Swap back if no match
                    selected_cell = None
                else:
                    selected_cell = (row, col)
            else:
                selected_cell = (row, col)
    
    clock.tick(30)

pygame.quit()
