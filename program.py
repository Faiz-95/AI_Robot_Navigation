import sys
import myFuncs as F

#object to initiate the program using the file name, file path , search method
class Program:
    def __init__(self, file_name, file_path, search_method):
        self.file_name = file_name
        self.file_path = file_path
        self.search_method = search_method
   
#will always run at the beginning of the program
if (__name__ == "__main__"):
    try:
        while True:
            file_name = sys.argv[1]
            if F.does_file_exist(file_name):
                file_path = f"./TestFiles/{file_name}"  #file stored in 'TestFiles' Directory
                break
            else:
                print("File doesn't exist in 'TestFiles' directory\n")
                sys.exit()

        while True:
            search_method = sys.argv[2].lower()

            #function to check if the search method is valid
            if F.is_search_method_valid(search_method):
                robot_program = Program(file_name, file_path, search_method)    #creates the program class            
                file_lines = F.list_of_file_lines(file_path)    #function to store each line of the file as an element in a list
                robot_map = F.generate_map(file_lines)  #function to generate the initial map based on file_lines list
                robot_map.print_map()   #function to print the initial map
                F.process_search_method(search_method,robot_map,file_name)    #function to process the file map based on the search method
                break
            else:
                print("Enter a valid search method\n")
                sys.exit()
    except IndexError:
        print("Enter valid arguments")


