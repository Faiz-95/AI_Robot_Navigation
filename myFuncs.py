import re
import os.path
import myMap as M
import bfs as B
import dfs as D
import gbfs as G
import astar as A
import cus1 as C1
import cus2 as C2

# Function to check if the file name entered by user exists
def does_file_exist(file_name):
    file_path = f"./TestFiles/{file_name}"
    if os.path.exists(file_path):
        return True
    return False



# Function to check if the search method entered by user is valid
def is_search_method_valid(search_method):
    methods = ["as","bfs","dfs","gbfs","cus1","cus2"]
    if search_method in methods:
        return True
    return False



# Function to read file and add each line as an element in a list
def list_of_file_lines(file_path):
    file = open(file_path, "r")
    return file.readlines()



# Function to generate the map based on the file_lines list
def generate_map(file_lines):
    for i in range(len(file_lines)):
        list_of_coordinates = []
        string_of_line = re.split(r'\D+', file_lines[i])    # Splits each element of the list based on whether the element is a digit
        # ['[5,11]\n'] ---> ['','5','11','']
        
        for value in string_of_line:
            # Checks if the element of the list contains a value or empty string
            if value:
                list_of_coordinates.append(int(value))  # Converts the string value to an integer

        # Condition to create the number of rows and columns if its the first row
        if i == 0:
            rows = list_of_coordinates[0]
            columns = list_of_coordinates[1]
            robot_map = M.Map(rows,columns)     # Creates the Map object using rows and columns as arguements
        robot_map.grid_values(i, list_of_coordinates)   # Creates the map using the values
    return robot_map    # Returns robot object



# Function to begin search method on the map generated
# Returns the number of nodes searched along with the final path
def process_search_method(search_method,robot_map,file_name):
    if search_method == "bfs":
        search = B.Bfs()
        result = B.begin_search(search,robot_map)
        method = "Breadth-First Search"
    elif search_method == "dfs":
        search = D.Dfs()
        result = D.begin_search(search,robot_map)
        method = "Depth-First Search"
    elif search_method == "gbfs":
        search = G.Gbfs()
        result = G.begin_search(search,robot_map)
        method = "Greedy Best-First Search"
    elif search_method == "as":
        search = A.As()
        result = A.begin_search(search,robot_map)
        method = "A* Search"
    elif search_method == "cus1":
        search = C1.Cus1()
        result = C1.begin_search(search,robot_map)
        method = "Custom 1 Search (Random Search)"
    elif search_method == "cus2":
        search = C2.Cus2()
        result = C2.begin_search(search,robot_map)
        method = "Custom 2 Search (Iterative Deepening A* Search)"
    print("File Name = ", file_name)
    print("Search Method = ",method)
    print(result)







