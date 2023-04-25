import time
import os

# Creating AS Search object
class As:
    def __init__(self):
        self.nodes = 0
        self.start_and_finish_exist = False
        self.reached_finish = False
        self.directions = []
        self.current_position = []
        self.adjacents = [] 
        self.not_visited = [] 
        self.visited = [] 
        self.final_direct_and_pos = []
        self.finish_positions = []



# Function to begin search and return the nodes and directions 
def begin_search(search, robot_map):
    find_start_and_end(search,robot_map)
    search.current_position = search.visited[0] # Assigning the current position to the start position

    while ((len(search.not_visited) >= 0) and (not search.reached_finish) and (search.start_and_finish_exist)):

        if search.not_visited:
            search.nodes += 1 # Each time it is looped, add 1 to the search node total

        lowest_manhattan_distance(search, robot_map)
        find_valid_adjacents(search, robot_map)
        adjacent_heuristics(search, robot_map)
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
                search.visited.append([[[0,0],search.directions],[i,j]]) # Considering start position to be a visited position
                # Each position within a list consists of 2 lists -> [[List1],[List2]]
                # List 1 = [[Distance from start, Total Distance],directions to position]
                # List 2 = [X coordinate, Y coordinate]
                found_start = True
            elif cell == "F":
                search.finish_positions.append([search.directions,[i,j]])
                found_finish = True

    search.start_and_finish_exist = found_start and found_finish



# Fuction to set the current position of the robot to the point with the lowest Manhattan Distance
def lowest_manhattan_distance(search, robot_map):

    # Condition to check if the not_visited list is empty
    if ((len(search.not_visited)) == 0):
        pos_list = search.visited # Will be true only for the first case when the program is initiated and the robot is at the start position 
    else:
        pos_list = search.not_visited # Will be true for rest of the cases

    lowest_dist = pos_list[0][0][0][1]
    lowest_manhattan_position_index = 0

    if pos_list:
        # Loop to check if the present manhattan distance is the least
        for i in range(len(pos_list)):
            if pos_list[i][0][0][1] < lowest_dist:
                lowest_dist = pos_list[i][0][0][1] # Assign the manhattan distance to value of the new position
                lowest_manhattan_position_index = i 
        
        search.current_position = pos_list[lowest_manhattan_position_index] # Update the current position to the position with the lowest manhattan value
        
        if search.not_visited:
            search.not_visited.pop(lowest_manhattan_position_index) # Remove the position with the lowest manhattan value from the positions list based on the index value
        else:
            search.visited.pop(lowest_manhattan_position_index)

        row, col = search.current_position[1]
        if robot_map.grid[row][col] not in ["S","F"]:
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



# Function to check the valid adjacent positions
def check_adjacent_value(direct, row_num, col_num, search, robot_map):
    search.directions = []

    # Condition to append an already existing direction to a position
    if search.current_position[0][1]:
        for i in search.current_position[0][1]:
            search.directions.append(i)
    search.directions.append(direct)

    # Condition to check whether the adjacent value is the Finish     
    if robot_map.grid[row_num][col_num] == "F":
        if not search.final_direct_and_pos: # Check to see if values already exist in the list
            search.adjacents.append([[search.current_position[0][0],search.directions],[row_num,col_num]]) 
            search.final_direct_and_pos = [search.directions,[row_num,col_num]] # Stores the directions and position of the final location
            search.reached_finish = True
            search.nodes += 1

    # Condition to check whether the adjacent value is an empty cell
    elif (robot_map.grid[row_num][col_num] == " "):
        search.adjacents.append([[search.current_position[0][0],search.directions],[row_num,col_num]]) 
        # Appends the manhattan distance, direction from start position to the adjacent position, x coordinate and y coordinate of the position
    


# Function to add the adjacent position to the beginning of the not_visited list
def adjacent_heuristics(search, robot_map):
    for adj in search.adjacents:
        adj_coords = adj[1] # Assigning the coordinates of each adjacent position

        # Condition to check if the adjacent position is the Finish or not
        if robot_map.grid[adj_coords[0]][adj_coords[1]] != "F":
            s_dist = adj[0][0][0] + 1 # Distance from start to adjacent position
            m_dist = manhattan_distance(search, adj_coords) # Calculate manhattan distance for that point
            # Pass the x and y coordinates also as arguements
            total_dist = s_dist + m_dist # Total distance from start and finish added

            # Check if the position exists in the not_visited or visited list
            if exists_in(search.not_visited, adj_coords, total_dist) or exists_in(search.visited, adj, total_dist):
                pass # Ignore adjacent cell as it already exists
            else:
                search.not_visited.append([[[s_dist,total_dist],adj[0][1]],[adj_coords[0],adj_coords[1]]])
                robot_map.grid[adj_coords[0]][adj_coords[1]] = "X" # Marks an empty cell with X to denote a position that has not been visited yet 

    search.visited.append(search.current_position) # Append the current position to the visited list
    


# Function to calculate manhattan distance of a position to the closest finish position
def manhattan_distance(search, coords):
    final_pos_coords = search.finish_positions[0][1]

    # Calculate the manhattan distance from a position to the first goal position
    man_dist_1 = abs(coords[0] - final_pos_coords[0]) + abs(coords[1] - final_pos_coords[1]) 
    
    # Loop to calculate manhattan distance for all finish positions and use the lowest one
    for other_finish_positions in search.finish_positions:
        man_dist_2 = abs(coords[0] - other_finish_positions[1][0]) + abs(coords[1] - other_finish_positions[1][1]) # Use abs() to obtain absolute value

        # Comparing manhattan distances of goal positions and returning the lowest one
        if man_dist_2 < man_dist_1:
            man_dist_1 = man_dist_2
    return man_dist_1



# Function to check if a position exists in a list
def exists_in(positions_list, coords, total_dist):
    for position in positions_list:
        if position[1] == coords:
            if (position[0][0][1] <= total_dist):
                return True
    return False






















