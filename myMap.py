import os
import time

# Creates the Map object
class Map:

    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns
        self.grid = [ [" "]*self.columns for i in range(self.rows)] # Creates a 2D array with empty strings
        # number of rows = number of lists
        # number of columns = number of elements in each list


    # Function to create the map based on values
    def grid_values(self,line_number, list_of_coordinates):
        if line_number == 0:
            pass    # Since we have already checked this condition in the previous function
            
        elif line_number == 1:  # Creates the start position of the robot
            if len(list_of_coordinates) == 2:
                self.grid[list_of_coordinates[1]][list_of_coordinates[0]] = "S"

        elif line_number == 2:  # Creates the finishing position(s) of the robot
            count = 0
            value = 0
            # Loop to ensure 2 positions are created if 2 coordinates are mentioned
            for i in list_of_coordinates:
                count += 1
                if count != 2:
                    value = i
                else:
                    self.grid[i][value] = "F"
                    count = 0

        else:  # Creates the walls
            for i in range(list_of_coordinates[1], list_of_coordinates[1] + list_of_coordinates[3]):
                for j in range(list_of_coordinates[0], list_of_coordinates[0] + list_of_coordinates[2]):
                    self.grid[i][j] = "\u2588"  # Unicode character for a Block 
                    pass


    # Function to print map 
    def print_map(self):
        print()
        for i in range(self.rows):
            print(" | ",end="")
            for j in range(self.columns):
                print(self.grid[i][j], end="")
                print(" | ", end="")
            print()
        print()






