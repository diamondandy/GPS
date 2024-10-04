"""Create routes between cities on a map."""

'''GPS.PY by Diamond Andy :]'''

import sys
import argparse

class City:
    
    def __init__(self, name):
        """This function just sets name to an attribute, and sets the neighbor attribute to an empty dictionary.

        Args:
            name (string): The name of the city
        """
        
        self.name = name 
        
        self.neighbors = {}    
        
    #repr = representation    
    def __repr__(self):
        """This function will return the name of the instance 

        Returns:
            str: returns the name attribute of the instance
        """
        
        return self.name
    
    
    def add_neighbor(self, neighbor, distance, interstate):
        """This function adds a neighbor to the city

        Args:
            neighbor (City): The City object that will be connected to this instance (and vice versa)
            distance (str): Represents the distance between two cities.
            interstate (str): Represents the interstate number that connects the two cities
        """
        
        if neighbor not in self.neighbors:
            
            self.neighbors[neighbor] = (distance, str(interstate))
            
        
            
            neighbor.add_neighbor(self, distance, str(interstate))
            
            
            
    
class Map:
    def __init__ (self, relationships):
        """ This function intializes a map object.

        Args:
            relationships (dict): A dictionary where the keys are individual cities and a list of tuples with string, distance and interstate.
        """
        
        self.cities = []
        
        for key in relationships:
            
            if key not in [c.name for c in self.cities]:
                
                city = City(key)
                
                self.cities.append(city)
                
            index_of_key = [c.name for c in self.cities].index(key)
            
            for neighbor, distance, interstate in relationships[key]:
            
                if neighbor not in [c.name for c in self.cities]:
                
                    neigh_bor = City(neighbor)
                
                    self.cities.append(neigh_bor)
                
                index_of_neighbor = [c.name for c in self.cities].index(neighbor)
            
                self.cities[index_of_neighbor].add_neighbor(self.cities[index_of_key], distance, interstate)
            
            
                   
    def __repr__(self):
        """This function just returns the cities string

        Returns:
            str: Returns the string representation of cities.
        """
        
        return str(self.cities)
    
    
        


#bfs stands for "Breadth-First Search"
def bfs(graph, start, goal):
    
    """Returns a list of strings (the cities) that we will on the shortest path between the start and goal cities"
    """
    
    explored = []
    
    queue = [[start]]
    
    while queue:
        
        pathway = queue.pop(0)
    
        last_node = pathway[-1]
        
        if last_node not in explored:
            
            city_names = [i.name for i in graph.cities]
            
            neighbors = graph.cities[city_names.index(str(last_node))].neighbors
            
            for neighbor in neighbors:
                
                new_path = list(pathway)
                
                new_path.append(neighbor)
                
                queue.append(new_path)
                
                if str(neighbor) == goal:
                    
                    return [str(city) for city in new_path] 
                
                explored.append(last_node)
                
    print(f"Path not found from {start} to {goal}")
                
    return None
            
            
    

#Theres a typo in the directions, graph is the same thing as "connections" stated in the parameters!
def main(start, destination, connections):
    """Runs the whole GPS system!

    Args:
        start (str): The start city in a road trip 
        destination (str): The destination city for a roadtrip 
        connections (_dict): A dictionary representing an adjecency list of cities and the cities to which they
connect

    Raises:
        Exception: if there is no path found

    Returns:
        string: A string that contains all of the same contents that we have printed out to the console/terminal.
    """
    
    
    connnections_of_map = Map(connections)
    
    instructions = bfs(connnections_of_map, start, destination)
    
    city_result = ''
    
    if instructions == None:
        
        raise Exception("No path was found")
    
    for i, city in enumerate(instructions):
        
        
        if i == 0:
            
            city_result += f'Starting at {start}'
            
        if i < len(instructions) - 1:
        
            
            next_city = instructions[i + 1]
            
            dict_of_neighbors = {}
            
            cities = [c.name for c in connnections_of_map.cities].index(city)
            
            neighbors = connnections_of_map.cities[cities].neighbors
            
            
            
            for key, value in neighbors.items():
                
                dict_of_neighbors[str(key)] = value
                
            distance, interstate = dict_of_neighbors[next_city]
            
            city_result += f'Drive {distance} miles on {interstate} towards {next_city}, then'
            
        if i == len(instructions) - 1:
            
            city_result += 'You will arrive at your destination'
            
    return city_result
            
            
            
    
        


def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis,", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 283, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "80"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76")],
        "Indianapolis": [("Columbus", 175, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 183, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburg": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 304, "76"), ("New York", 391, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburg", 107, "76")], #COMEBACK
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence,", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 101, "95"), ("New York", 95, "95")]
    }
    
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)