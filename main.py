import pygame
import random
import time

starting_time = time.time()

pygame.init()

WIDTH = HEIGHT = 600

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock   = pygame.time.Clock()

pygame.display.set_caption("Maze Generator")
pygame.display.set_icon(pygame.image.load("images/maze.png"))

process_interrupted = maze_created = False
amount_of_visited_cells = 0

maze_size     = 50
cells         = [[["0", "0", "0", "0", "0", False] for w in range(maze_size)] for h in range(maze_size)]
current_cell  = (0, 0)
visited_cells = []

while not process_interrupted:
    display.fill((255, 255, 255))

    if not maze_created:
        pygame.display.set_caption(f"Maze Generator    {(amount_of_visited_cells / (maze_size**2)*100):.1f} %")

        # Get all unvisited neighbour cells
        possible_moves = []
        if current_cell[1] > 0 and cells[current_cell[1]-1][current_cell[0]][-1] == False:
            possible_moves.append("1")
        if current_cell[0] < maze_size-1 and cells[current_cell[1]][current_cell[0]+1][-1] == False:
            possible_moves.append("2")
        if current_cell[1] < maze_size-1 and cells[current_cell[1]+1][current_cell[0]][-1] == False:
            possible_moves.append("3")
        if current_cell[0] > 0 and cells[current_cell[1]][current_cell[0]-1][-1] == False:
            possible_moves.append("4")
        
        # Pick any of the unvisited neighbours. If there is no unvisited neighbour, move backwards
        next_move = random.choice(possible_moves) if len(possible_moves) > 0 else "5"
        # Set the direction for the current cell to the corresponding index
        cells[current_cell[1]][current_cell[0]][int(next_move)-1] = next_move
        # Mark the current cell as visited
        if cells[current_cell[1]][current_cell[0]][-1] != True:
            cells[current_cell[1]][current_cell[0]][-1] = True
            amount_of_visited_cells += 1

        if next_move != "5":
            visited_cells.append(current_cell)

        # Moving the current cell
        if next_move == "1":
            current_cell = (current_cell[0], current_cell[1]-1)
        elif next_move == "2":
            current_cell = (current_cell[0]+1, current_cell[1])
        elif next_move == "3":
            current_cell = (current_cell[0], current_cell[1]+1)
        elif next_move == "4":
            current_cell = (current_cell[0]-1, current_cell[1])
        elif next_move == "5":
            # Go back from the current cell until back in the starting point
            if len(visited_cells) > 0:
                current_cell = visited_cells[-1]
                visited_cells.pop()
            else:
                # If cannot go back anymore, the maze is finished
                pygame.display.set_caption(f"Maze Generator    {(amount_of_visited_cells / (maze_size**2)*100):.1f} %    Finished in {(time.time() - starting_time):.3f} s")
                maze_created = True

    # Draw the maze
    x = y = 0
    cell_height = HEIGHT/len(cells)
    for row in range(len(cells)):
        cell_width = WIDTH/len(cells[row])
        for col in range(len(cells[row])):
            
            # Cursor
            if not maze_created and col == current_cell[0] and row == current_cell[1]:
                pygame.draw.rect(display, (200, 200, 200), (x, y, cell_width, cell_height))

            # Unvisited cell
            if cells[row][col][-1] == False:
                pygame.draw.rect(display, (140, 200, 255), (x, y, cell_width, cell_height))
            else:
                # Visited cells' borders
                if y > 0 and y < HEIGHT:
                    if cells[row][col][0] != "1" and cells[row-1][col][2] != "3":
                        pygame.draw.line(display, (0, 0, 0), (x, y), (x+cell_width, y), 2)
                
                if x > 0 and x < WIDTH:
                    if cells[row][col-1][1] != "2" and cells[row][col][3] != "4":
                        pygame.draw.line(display, (0, 0, 0), (x, y), (x, y+cell_height), 2)
            
            x += cell_width
        x = 0
        y += cell_height

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_interrupted = True
            break

    pygame.display.update()
    # clock.tick(20)    # Speed limiter

pygame.quit()
    