import pygame
from random import choice

# DO NOT MODIFY CODE ABOVE THIS LINE -----------------------------------------------------------------------------------

WIDTH, HEIGHT            = 600, 600     # Window size
maze_size_w, maze_size_h = 20, 20       # Maze size

# DO NOT MODIFY CODE BELOW THIS LINE -----------------------------------------------------------------------------------

process_paused           = False
maze_created             = False
amount_of_visited_cells  = 0    # Used to calculate the percentage of the maze that has been generated
finish_flag              = -1
cells                    = [[["0", "0", "0", "0", "0", False] for _ in range(maze_size_w)] for _ in range(maze_size_h)]
current_cell             = (0, 0)  # This is where the maze generator will start generating
visited_cells            = []
open_nodes               = {(0, 0): (0, 0)}
closed_nodes             = []
current_node             = -1
maze_solved              = False
path_drawn               = False
path                     = []
path_map                 = {}
current_step             = (maze_size_w - 1, maze_size_h - 1)


def generate_maze():
    global maze_created, process_paused, current_cell, amount_of_visited_cells

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

        # Pick any of the unvisited neighbours. If there are no unvisited neighbours, move backwards
        next_move = choice(possible_moves) if len(possible_moves) > 0 else "5"
        # Set the direction for the current cell to the corresponding index
        cells[current_cell[1]][current_cell[0]][int(next_move)-1] = next_move
        # Mark the current cell as visited
        if not cells[current_cell[1]][current_cell[0]][5]:
            cells[current_cell[1]][current_cell[0]][5] = True
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
                # If you cannot go back anymore, the maze is finished
                maze_created = True


def get_available_neighbours(node: tuple):
    # Get all available neighbour cells
    # 1 up, 2 down, 3 left, 4 right
    available_neighbours = []

    # The cell above
    if node[1] > 0 and (node[0], node[1] - 1) not in closed_nodes:
        if cells[node[1]][node[0]][0] == "1" or cells[node[1] - 1][node[0]][2] == "3":
            available_neighbours.append((node[0], node[1] - 1))

    # The cell below
    if node[1] < maze_size_h - 1 and (node[0], node[1] + 1) not in closed_nodes:
        if cells[node[1]][node[0]][2] == "3" or cells[node[1] + 1][node[0]][0] == "1":
            available_neighbours.append((node[0], node[1] + 1))

    # The cell to the left
    if node[0] > 0 and (node[0] - 1, node[1]) not in closed_nodes:
        if cells[node[1]][node[0]][3] == "4" or cells[node[1]][node[0] - 1][1] == "2":
            available_neighbours.append((node[0] - 1, node[1]))

    # The cell to the right
    if node[0] < maze_size_w - 1 and (node[0] + 1, node[1]) not in closed_nodes:
        if cells[node[1]][node[0]][1] == "2" or cells[node[1]][node[0] + 1][3] == "4":
            available_neighbours.append((node[0] + 1, node[1]))

    return available_neighbours


def solve_maze():
    # A* algorithm, to find the shortest path from the starting point to the end point
    # Starting point: (0, 0)
    # End point: (maze_size_w-1, maze_size_h-1)
    # g = distance from the starting point
    # h = abs(current_cell.x - goal.x) + abs(current_cell.y - goal.y)
    # f = g + h
    # If there are multiple same f values, choose the one with the lowest h value.

    global open_nodes, closed_nodes, current_node, maze_solved, path_drawn, path_map, path

    if maze_created is False or maze_solved is True or process_paused is True:
        return

    # Set the current node to the node with the lowest f value
    if len(open_nodes) >= 2:
        open_nodes_f_cost = {}
        open_nodes_h_cost = {}

        for node in open_nodes:
            open_nodes_f_cost[node] = open_nodes[node][0]
            open_nodes_h_cost[node] = open_nodes[node][0]

        node_with_lowest_f_cost = min(open_nodes_f_cost, key=open_nodes_f_cost.get)
        node_with_lowest_h_cost = min(open_nodes_h_cost, key=open_nodes_h_cost.get)

        # Get nodes that have the same f cost
        same_f_cost = []
        for node in open_nodes:
            if node != node_with_lowest_f_cost and open_nodes[node] == open_nodes[node_with_lowest_f_cost]:
                same_f_cost.append(node)

        # If there are multiple same f values, choose the one with the lowest h value.
        if len(same_f_cost) > 1:
            current_node = node_with_lowest_h_cost
        else:
            current_node = node_with_lowest_f_cost

    else:
        if len(open_nodes) > 0:
            current_node = list(open_nodes.keys())[0]

    if current_node not in closed_nodes:
        closed_nodes.append(current_node)

    if current_node in open_nodes:
        del open_nodes[current_node]

    if current_node == (maze_size_w-1, maze_size_h-1):
        maze_solved = True

    available_neighbours = get_available_neighbours(current_node)

    for neighbour in available_neighbours:
        # Calculate the f cost for each neighbour
        # g = hypotenuse of the distance from the starting point to the current node
        # h = hypotenuse of the distance from the current cell to the end cell
        open_nodes[neighbour] = (
            # f = g + h
            ((neighbour[0]-current_node[0])**2 + (neighbour[1]-current_node[1])**2)**0.5 +
            ((neighbour[0]-(maze_size_w-1))**2 + (neighbour[1]-(maze_size_h-1))**2)**0.5,

            # h - This value is used, if there are multiple nodes with the same f value to determine which one to choose
            ((neighbour[0] - (maze_size_w - 1)) ** 2 + (neighbour[1] - (maze_size_h - 1)) ** 2) ** 0.5
        )

        # When entering a new node, set the neighbours to reflect to the current node.
        # This is needed to draw the path later.
        path_map[neighbour] = current_node


def generate_and_solve_maze():
    global current_step, path_drawn, path

    # These functions will not run if they are already finished.
    generate_maze()
    solve_maze()

    if maze_created is True and process_paused is False:
        # Remove the gap between the end of the path and the current node
        path = [current_node]

        if current_node != -1 and current_node != (0, 0):
            current_step = path_map[current_node]

            while current_step != (0, 0):
                path.append(current_step)
                current_step = path_map[current_step]

        # Remove the gap between the start of the path and the starting point
        path.append((0, 0))


def draw_maze(display: pygame.Surface, cell_width, cell_height):
    x = y = 0

    for row in range(len(cells)):
        for col in range(len(cells[row])):

            # Unvisited cell
            if not cells[row][col][-1]:
                pygame.draw.rect(display, (140, 200, 255), (int(x), int(y), int(cell_width), int(cell_height)))
            else:
                # Visited cells' borders
                if 0 < y < HEIGHT:
                    if cells[row][col][0] != "1" and cells[row - 1][col][2] != "3":
                        pygame.draw.line(display, (0, 0, 0), (x, y), (x + cell_width, y), 2)

                if 0 < x < WIDTH:
                    if cells[row][col - 1][1] != "2" and cells[row][col][3] != "4":
                        pygame.draw.line(display, (0, 0, 0), (x, y), (x, y + cell_height), 2)

            # Cursor
            if not maze_created and col == current_cell[0] and row == current_cell[1]:
                pygame.draw.rect(display, (150, 150, 150), (int(x), int(y), int(cell_width), int(cell_height)))

            x += cell_width

        x = 0
        y += cell_height


def draw_path(display: pygame.Surface, cell_width, cell_height):
    global finish_flag
    if finish_flag == -1:
        finish_flag = pygame.transform.smoothscale(
            pygame.image.load("images/finish.jpg"), (int(cell_width), int(cell_height))
        )

    if maze_created is False:
        return

    path_color     = (255, 0, 0)
    path_thickness = 2

    if maze_solved is True:
        path_color     = (0, 255, 0)
        path_thickness = 4

    # Draw the finish flag
    display.blit(finish_flag, (int((maze_size_w-1)*cell_width) + 2, int((maze_size_h-1)*cell_height) + 2))

    # Connect the cells in the path
    if len(path) > 1:
        for i in range(len(path) - 1):
            pygame.draw.line(
                display, path_color, (
                    path[i][0] * cell_width + cell_width / 2,
                    path[i][1] * cell_height + cell_height / 2
                ), (
                    path[i + 1][0] * cell_width + cell_width / 2,
                    path[i + 1][1] * cell_height + cell_height / 2
                ), path_thickness
            )

    # Starting point
    pygame.draw.rect(
        display, path_color, (
            cell_width / 4, cell_height / 4, cell_width / 2, cell_height / 2
        )
    )

    # Current point
    pygame.draw.rect(
        display, path_color, (
            int(current_node[0] * cell_width + (cell_width / 4)),
            int(current_node[1] * cell_height + (cell_height / 4)),
            int(cell_width / 2),
            int(cell_height / 2)
        )
    )


def draw_maze_and_path(display: pygame.Surface):
    cell_width  = WIDTH / len(cells[0])
    cell_height = HEIGHT / len(cells)

    # Draw the maze
    draw_maze(display, cell_width, cell_height)

    # Draw the path
    draw_path(display, cell_width, cell_height)


def reset_maze():
    global cells, current_cell, visited_cells, amount_of_visited_cells, process_paused, maze_created, maze_solved,\
        path_drawn, current_node, open_nodes, closed_nodes, path, path_map, current_step

    cells = [
        [["0", "0", "0", "0", "0", False] for _ in range(maze_size_w)] for _ in range(maze_size_h)
    ]
    current_cell            = (0, 0)
    visited_cells           = []
    amount_of_visited_cells = 0
    process_paused          = False
    maze_created            = False

    maze_solved  = False
    path_drawn   = False
    current_node = -1
    open_nodes   = {(0, 0): 0}
    closed_nodes = []
    path         = []
    path_map     = {}
    current_step = (maze_size_w - 1, maze_size_h - 1)


def main():
    global process_paused, amount_of_visited_cells, current_node

    pygame.init()

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock   = pygame.time.Clock()
    pygame.display.set_caption("Maze")
    pygame.display.set_icon(pygame.image.load("images/maze.png"))

    speed_limit = 0

    process_interrupted = False

    while not process_interrupted:
        # Calculate the approximate advancement of the recursive backtracking algorithm
        generating_percentage = amount_of_visited_cells / (maze_size_w * maze_size_h) * 100

        # Calculate the approximate advancement of the A* algorithm
        solving_percentage = 0

        if current_node != -1:
            distance_from_start = ((0 - current_node[1]) ** 2 + (0 - current_node[0]) ** 2) ** 0.5
            distance_from_end = ((maze_size_w - 1) ** 2 + (maze_size_h - 1) ** 2) ** 0.5
            solving_percentage = (distance_from_start / distance_from_end) * 100

        # Set the window title
        pygame.display.set_caption(
            f"Maze    {generating_percentage:.1f} % - {solving_percentage:.1f} %" +
            f"    {speed_limit if speed_limit != 0 else 'unltd.'} fps    {'PAUSED' if process_paused else ''}"
        )

        # Clear the screen before drawing the new frame
        display.fill((255, 255, 255))

        generate_and_solve_maze()
        draw_maze_and_path(display)

        # Handle keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                process_interrupted = True
                break

            if event.type == pygame.KEYDOWN:
                # Change generation/solving speed
                if event.key == pygame.K_UP:
                    if speed_limit >= 10:
                        speed_limit += 10
                    else:
                        speed_limit += 2
                if event.key == pygame.K_DOWN:
                    if speed_limit > 10 or speed_limit == 0:
                        speed_limit -= 10
                    else:
                        speed_limit -= 2
                speed_limit = speed_limit % 110

                # Pause / Play
                if event.key == pygame.K_SPACE:
                    process_paused = not process_paused

                # Restart
                if event.key == pygame.K_RETURN:
                    reset_maze()

        pygame.display.update()
        clock.tick(speed_limit)

    pygame.quit()


if __name__ == "__main__":
    main()
