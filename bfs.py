import time
import os

# Creating BFS Search object
class Bfs:
    def __init__(self):
        self.nodes = 0
        self.start_and_finish_exist = False
        self.reached_finish = False
        self.directions = []
        self.current_position = []
        self.adjacents = []
        self.not_visited = []
        self.final_direct_and_pos = []
        self.finish_positions = []



# Function to begin search and return the nodes and directions 
def begin_search(search, robot_map):
    find_start_and_end(search,robot_map)

    while ((len(search.not_visited) >= 0) and (not search.reached_finish) and (search.start_and_finish_exist)):

        if search.final_direct_and_pos:
            if search.current_position[1] == search.final_direct_and_pos[1]: # Check to see if the robot's current position is the finish position
                search.reached_finish = True
                break

        if search.not_visited:
            search.nodes += 1 # Each time it is looped, add 1 to the search node total

        visit_position(search,robot_map)
        find_valid_adjacents(search,robot_map)
        add_adjacents_to_not_visited(search,robot_map)
        os.system('cls' if os.name == 'nt' else 'clear')
        robot_map.print_map()
        time.sleep(0.5)
    
    x_nodes = 0
    for row in robot_map.grid:
        for column in row:
            if column == "X": # Check to see which nodes have not been searched yet 
                x_nodes += 1 

    # Condition to check whether the finish was found to return a result
    if search.reached_finish:
        direct_str = '; '.join(str(i) for i in search.final_direct_and_pos[0])
        return f"Number of nodes in search tree = {search.nodes + x_nodes}\nNumber of nodes searched = {search.nodes}\nDirections = {direct_str}"
    else:
        return "No solution found."



# Function to locate start and end of the robot
def find_start_and_end(search, robot_map):
    found_start = False
    found_finish = False

    for i, row in enumerate(robot_map.grid):
        for j, cell in enumerate(row):
            if cell == "S":
                search.current_position = [search.directions, [i, j]] 
                found_start = True
            elif cell == "F":
                search.finish_positions.append([i, j])
                found_finish = True

    search.start_and_finish_exist = found_start and found_finish



# Function to change the state of the positions
def visit_position(search, robot_map):
    if ((len(search.not_visited)) > 0):
        search.current_position = search.not_visited[0] # Since bfs follows FIFO, we always assign current position to the first position that is not visited
        search.not_visited.pop(0) # Remove the position from the not_visited list once the robot moves to the new position
        row, col = search.current_position[1]
        if robot_map.grid[row][col] != "F":
            robot_map.grid[row][col] = "-" # Update the new position with a '-' indicating that the robot has moved there



# Function to find the valid adjacents around a position
def find_valid_adjacents(search, robot_map):
    search.adjacents.clear()
    row, col = search.current_position[1]

    # Robot follows UP-LEFT-DOWN-RIGHT priority hence directions in that order
    directions = ["up", "left", "down", "right"]
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    # Up = Row Number - 1
    # Left = Row Number - 1
    # Down = Row Number + 1
    # Right = Column Number + 1
    
    for direction, move in zip(directions, moves):
        new_row, new_col = row + move[0], col + move[1]
        if (0 <= new_row < robot_map.rows and 0 <= new_col < robot_map.columns):
            check_adjacent_value(direction, new_row, new_col, search, robot_map)

    # Check to see whether the adjacent position already exists in the not_visited list, if not append it to the not_visited list
    for i in search.adjacents: 
        if i not in search.not_visited:
            search.not_visited.append(i)



# Function to check the valid adjacent positions
def check_adjacent_value(new_direction, row_num, col_num, search,robot_map):
    search.directions = []

    # Condition to append an already existing direction to a position
    if search.current_position[0]:
        for i in search.current_position[0]:
            search.directions.append(i)
    search.directions.append(new_direction)

    # Condition to check whether the adjacent value is the Finish    
    if robot_map.grid[row_num][col_num] == "F":
        if not search.final_direct_and_pos: # Check to see if values already exist in the list
            search.adjacents.append([search.directions,[row_num,col_num]])
            search.final_direct_and_pos = [search.directions,[row_num,col_num]] # Stores the directions and position of the final location

    # Condition to check whether the adjacent value is an empty cell
    elif robot_map.grid[row_num][col_num] == " ":
        search.adjacents.append([search.directions,[row_num,col_num]]) # Appends the direction from start position to the adjacent position



# Function to add the adjacent position to the end of the not_visited list
def add_adjacents_to_not_visited(search,robot_map):
    for adj in search.adjacents:
        for nv in search.not_visited:
            if nv[1] == adj[1]:
                search.not_visited.remove(nv) 
        search.not_visited.append(adj) # Inserts the position to the end of the not_visited list
        if robot_map.grid[adj[1][0]][adj[1][1]] != "F":
            robot_map.grid[adj[1][0]][adj[1][1]] = "X" # Marks an empty cell with X to denote a position that has not been visited yet 


