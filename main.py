# Import ONLY the items needed for a slightly better performance
from pygame         import init, KEYDOWN, K_UP, K_DOWN, K_SPACE, K_RETURN, QUIT, quit
from pygame.display import set_mode, set_caption, set_icon, update
from pygame.time    import Clock
from pygame.image   import load
from pygame.draw    import rect, line
from pygame.event   import get

from random         import choice
from time           import time

starting_time = ending_time = time()    # -> time.time()
pause_starting_time = pause_duration = 0

init()  # -> pygame.init()

WIDTH, HEIGHT            = 600, 600
maze_size_w, maze_size_h = 50, 50
speed_limit = 0

display = set_mode((WIDTH, HEIGHT))  # -> pygame.display.set_mode()
clock   = Clock()                    # -> pygame.time.Clock()

set_caption("Maze Generator")        # -> pygame.display.set_caption()
set_icon(load("images/maze.png"))    # -> pygame.display.set_icon()

process_interrupted = process_paused = maze_created = False
amount_of_visited_cells = 0

cells         = [[["0", "0", "0", "0", "0", False] for _ in range(maze_size_w)] for _ in range(maze_size_h)]
current_cell  = (0, 0)
visited_cells = []

while not process_interrupted:
    # -> pygame.display.set_caption()
    set_caption(f"Maze Generator    {(amount_of_visited_cells / (maze_size_w*maze_size_h)*100):.1f} %    {speed_limit if speed_limit != 0 else 'unltd.'} T/S    {f'Finished in {(ending_time - starting_time - pause_duration):.3f} s    ' if maze_created else ''}{'PAUSED' if process_paused else ''}")

    display.fill((255, 255, 255))

    if not maze_created and not process_paused:
        # Get all unvisited neighbour cells
        possible_moves = []
        if current_cell[1] > 0 and not cells[current_cell[1]-1][current_cell[0]][-1]:
            possible_moves.append("1")
        if current_cell[0] < maze_size_w-1 and not cells[current_cell[1]][current_cell[0]+1][-1]:
            possible_moves.append("2")
        if current_cell[1] < maze_size_h-1 and not cells[current_cell[1]+1][current_cell[0]][-1]:
            possible_moves.append("3")
        if current_cell[0] > 0 and not cells[current_cell[1]][current_cell[0]-1][-1]:
            possible_moves.append("4")
        
        # Pick any of the unvisited neighbours. If there is no unvisited neighbour, move backwards
        next_move = choice(possible_moves) if len(possible_moves) > 0 else "5"
        # Set the direction for the current cell to the corresponding index
        cells[current_cell[1]][current_cell[0]][int(next_move)-1] = next_move
        # Mark the current cell as visited
        if not cells[current_cell[1]][current_cell[0]][-1]:
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
                ending_time = time()
                maze_created = True

    # Draw the maze
    x = y = 0
    cell_height = HEIGHT/len(cells)
    for row in range(len(cells)):
        cell_width = WIDTH/len(cells[row])
        for col in range(len(cells[row])):
            
            # Unvisited cell
            if not cells[row][col][-1]:
                rect(display, (140, 200, 255), (int(x), int(y), int(cell_width), int(cell_height)))  # -> pygame.draw.rect()
            else:
                # Visited cells' borders
                if 0 < y < HEIGHT:
                    if cells[row][col][0] != "1" and cells[row-1][col][2] != "3":
                        line(display, (0, 0, 0), (x, y), (x+cell_width, y), 2)   # -> pygame.draw.line()
                
                if 0 < x < WIDTH:
                    if cells[row][col-1][1] != "2" and cells[row][col][3] != "4":
                        line(display, (0, 0, 0), (x, y), (x, y+cell_height), 2)  # -> pygame.draw.line()

            # Cursor
            if not maze_created and col == current_cell[0] and row == current_cell[1]:
                rect(display, (150, 150, 150), (int(x), int(y), int(cell_width), int(cell_height)))  # -> pygame.draw.rect()
            
            x += cell_width
        x = 0
        y += cell_height

    for event in get():  # -> pygame.event.get()
        if event.type == QUIT:
            process_interrupted = True
            break
        
        if event.type == KEYDOWN:
            # Change generation speed / TPS (ticks per second)
            if event.key == K_UP:
                speed_limit += 10
            if event.key == K_DOWN:
                speed_limit -= 10
            speed_limit = speed_limit % 110

            # Pause / Play
            if event.key == K_SPACE:
                process_paused = not process_paused

                if not maze_created:
                    if process_paused:
                        pause_starting_time = time()                    # -> time.time()
                    elif not process_paused:
                        pause_duration += time() - pause_starting_time  # -> time.time()
            
            if event.key == K_RETURN:
                # Replay / Reset
                starting_time = ending_time = time()    # -> time.time()
                pause_starting_time = pause_duration = 0

                cells         = [[["0", "0", "0", "0", "0", False] for _ in range(maze_size_w)] for _ in range(maze_size_h)]
                current_cell  = (0, 0)
                visited_cells = []

                amount_of_visited_cells = 0
                process_paused = maze_created = False

    update()    # -> pygame.display.update()
    clock.tick(speed_limit)

quit()  # -> pygame.quit()
