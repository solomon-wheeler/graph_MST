import pygame
import time
from random import randint
import math


class graph:
    def __init__(self, nodes):
        self.num_nodes = int(nodes)
        self.matrix = [[0 for height in range(nodes)] for width in range(nodes)]
        self.nodes_cords = []
        # [start node][end node]

    # Below creates a random matrix The function will overwtie and edges already made, so the number of times is not
    # always equal to the number of times it runs
    def create_random(self, number_of_edges):
        for x in range(0, number_of_edges):
            first_node = randint(0, self.num_nodes - 1)  # -1 becuase num_nodes starts at 1 not 0
            last_node = randint(0, self.num_nodes - 1)
            weight = float(randint(0, 10))
            self.matrix[first_node][last_node] = weight
            self.matrix[last_node][
                first_node] = weight  # It does this twice because the randomly created edges aren't directional, so they can be traversed in either direction

    # This is called from main if the user wants to add the edges in the gaph themselves
    def add_edges(self):
        add = True  # This is set so edges are added until the user is done, at which point its set to false and no more edges are added
        print("The first node is called 0, and this goes up to the number of nodes you have chosen  -1")
        while add:
            first_node = int(input("What is the node this edge starts at?"))
            last_node = int(input("What is the node this edge ends at?"))
            weight = float(input("What is the weight of this node"))
            directional = str(input("Is this a one way line? (Y/N)"))
            if -1 < first_node < self.num_nodes and -1 < last_node < self.num_nodes:  # checks the users input is valid
                self.matrix[first_node][last_node] = weight
            else:
                print(
                    "That wasn't a valid input remember the naming of the nodes goes from 0 to total -1, and make "
                    "sure you only input this number")
            if directional == "N":
                self.matrix[last_node][
                    first_node] = weight  # From is this a one way line? IF not then the edge needs to be added to the matrix again because it goes from start to end node and end node to start node
            done = str(input("Input D to finish, or anythin else to add more nodes"))
            if done == "D":
                add = False

    def print_adjacency_matrix(self):
        for x in range(len(self.matrix)):
            print(self.matrix[x])

    # This creates the cordinates for where the nodes are, they are roughly placed in a circle, because this means no edges will go over nodes
    def create_node_coordinate(self, x, y):
        x = x - 20  # So the circle doen't touch the edges
        radius = int((x / 2) * 0.95)  # so circle dosent touch the edge
        amount_of_values = len(self.matrix)  # This is the number of nodes we have, we could alternatively use num nodes
        mid_x = int(x / 2)  # The midpoint of the screen in x axis
        mid_y = int(y / 2)  # ^^
        bottom = mid_x - radius  # This is the lowest x value in the cirlce
        diameter = radius * 2
        num_to_run = math.ceil(amount_of_values / 2)
        for x in range(0, num_to_run):  # This adds the edges
            x_cord = math.ceil(bottom + ((diameter / (
                    amount_of_values / 2)) * x))  # Bottom is lowest x value, which is divided by the amount of values /2 ( because we add to nodes for each x cordinate) then mutipled by which node we are currently dealing with to get its x cordinate
            y_value = math.ceil(math.sqrt((radius ** 2) - ((
                                                                   x_cord - mid_x) ** 2)))  # This uses the circle equation to find the y value since x^2 + y^2 = R^2 we can reagrane this to find y since we know x and R
            y_alt_cord = int(
                mid_y - y_value)  # This is just the negative version since the circle is centered at origin this will also be a point on the circle, means we have to go through the loop less times
            y_cord = int(mid_y + y_value)  # this ius the positive y value

            self.nodes_cords.append(
                [x_cord, y_cord, x])  # Adds the cordinates aswell as the x value, which is the number  of the node
            self.nodes_cords.append([x_cord, y_alt_cord,
                                     amount_of_values - x])  # amount of values - x just means that since we only run the for loop n/2 times all nodes are labbeled
        if 0 == amount_of_values % 2:  # For odd number the math.ceil function will mean we make the correct ammount,
            # for even values we add in the extra one here
            self.nodes_cords.append([mid_x + radius, mid_y, num_to_run])

    # This finds all of the edges on the graph and draws them on
    def find_edges(self):
        start_nodes_done = 0
        end_nodes_done = 0
        for each_start_node in self.matrix:
            for each_end_node in range(self.num_nodes):
                if each_start_node[
                    each_end_node] != 0 and start_nodes_done != end_nodes_done:  # If equal to 0 then there is no edge here, and if start_nodes done = end nodes done then this is an edge going to itself, which this program dosen't support at the moment
                    # todo make this more effective at finding nodes not just not equal to 0
                    if self.matrix[end_nodes_done][start_nodes_done] == self.matrix[start_nodes_done][
                        end_nodes_done]:  # If these values are the same then there are edges with the same weight from start to end and end to start, so this is not a direcitonal node
                        self.draw_edges(start_nodes_done, end_nodes_done, "Not Directional",
                                        self.matrix[end_nodes_done][start_nodes_done])
                    else:
                        self.draw_edges(start_nodes_done, end_nodes_done, "Directional",
                                        self.matrix[end_nodes_done][start_nodes_done])

                end_nodes_done += 1
            end_nodes_done = 0  # Resets every time we go to a new start node
            start_nodes_done += 1
        pygame.display.flip()  # one we've added all edges we show them on the display

    def draw_edges(self, node1, node2, type, weight):
        found = 0  # set to zero, we add one each time and then when it reachers to we know we have found both
        # todo test to check the same node is never being found twice
        for this_node in self.nodes_cords:
            if node1 == this_node[2]:
                cordinate_1 = [this_node[0], this_node[1]]
                found += 1
            elif node2 == this_node[2]:
                cordinate_2 = [this_node[0], this_node[1]]
                found += 1
            if found == 2:
                break
        x_dif = cordinate_2[0] - cordinate_1[0]  # This is the differnece between the two nodes
        y_dif = cordinate_2[1] - cordinate_1[1]
        # x_dif = 0 - x_dif
        # y_dif = 0 - y_dif
        num_location = [cordinate_1[0] + int((0.12 * x_dif)), cordinate_1[1] + int((
                0.12 * y_dif))]  # This finds a point just after the start of the line to add the weight on, this is the most clear method I have found for showing the weights, but there might be a better method

        if type == "Directional":  # THis is a pep violation but seems to make more sense this way
            this_line_colour = (255, 0, 0)
            size = 2
        elif type == "Not Directional":
            this_line_colour = (0, 255, 0)
            size = 2
        elif type == "Highlight":
            this_line_colour = (255, 192, 203)
            size = 5
        edge_weight = my_font.render(str(weight), 20, (255, 255, 255))
        screen.blit(edge_weight, num_location)  # Draws the weight of the edge
        pygame.draw.line(screen, this_line_colour, cordinate_1, cordinate_2,
                         size)  # Draws the line between the two nodes

    def primm_2(self):
        primms_matrix = self.matrix  # Creates a seperate matrix to work on for furture compatiablity where I might add differnt MST algorithms
        first_node = int(input("What Node would you like to start at?"))
        visited = [
            first_node]  # since we're starting at this node we don't need to find a way to it so it ahs already been visited
        num_visted = 1  # We've already vistied the first node
        while num_visted != self.num_nodes:
            found = False  # In case we don't find any new nodes to go to, this will happen if there's a subgraph within the graph
            for start_node in visited:
                lowest_weight = math.inf  # Lowest weight set to infinty
                for end_node in range(0, self.num_nodes):
                    if end_node not in visited:
                        if primms_matrix[start_node][end_node] < lowest_weight and primms_matrix[start_node][
                            end_node] != 0:
                            next = [start_node,
                                    end_node]  # The next edge to travese, will be updated if a new lower edge is found
                            lowest_weight = primms_matrix[start_node][end_node]
                            found = True
            if found == False:
                print(
                    "It seems there was no way to get to some of the nodes so the minium spanning tree has been created for the accesible nodes")
                break
            num_visted += 1
            visited.append(next[1])
            print(next)
            time.sleep(1)
            self.draw_edges(next[0], next[1], "Highlight", lowest_weight)
            # print(visited)
            pygame.display.flip()
            pygame.event.pump()  # Gets events for pygame window

# Takes all of the cordiantes of the ndoes and draws them on the pygame screen
def draw_nodes(cords):
    for working_node in cords:
        x_coordinate = working_node[0]
        y_coordinate = working_node[1]
        pygame.draw.circle(screen, (255, 165, 0), (x_coordinate, y_coordinate), 5)
        node_name = my_font.render(str(working_node[2]), 5, (255, 255, 255))
        screen.blit(node_name, (x_coordinate + 5, y_coordinate + 5))

    pygame.display.flip()


# Checks user hasn't inputed anything on the pygame window
def pygame_update_screen_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    pygame.event.pump()


# main
x = 600
y = 600  # Nodes are placed using a circle so if this is too small some will be hidden
# pygame setup
pygame.init()
my_font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
pygame.display.set_caption("Graph")
screen = pygame.display.set_mode((x, y))
number_of_nodes_choice = int(input("How many nodes does the graph have?"))
pygame_update_screen_inputs()

this_graph = graph(number_of_nodes_choice)
this_graph.create_node_coordinate(x, y)

draw_nodes(this_graph.nodes_cords)
if str(input("Would you like the program to create a matrix for you (1) or would you like to make your own(2)")) == "1":
    number_of_edeges_choice = int(input("How many times would you like it to randomly assign edges?"))
    this_graph.create_random(number_of_edeges_choice)
else:
    this_graph.add_edges()
pygame_update_screen_inputs()
this_graph.find_edges()
this_graph.print_adjacency_matrix()
this_graph.primm_2()

running = True
while running:
    pygame_update_screen_inputs()
