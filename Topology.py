from DistanceVector import *
import csv

#There is a lot of code in this file, but it's mostly just parsing the configuration file 
# and running the topology.
# There is one class in this file, Topology, which represents the entire network topology. 
# It has a method to load the topology from a configuration file,
# It appears that there is more code to be added to the Topology class, 
# such as methods to get the nodes and edges of the topology,

class Topology(object):
    def __init__(self, conf_file):
        """Initialize the topology with a configuration file."""
        self.topodict = {}
        self.nodes = []
        self.topo__from__conf_file(conf_file)

    def topo__from__conf_file(self, conf_file):
        """Load the topology from a configuration file."""
        input_file = open(conf_file, "rb")

        topology_data = csv.reader(input_file)
        for row in topology_data:
            if len(row) == 0:
                ''' Empty row '''
                continue
            if row[0].startswith('#'):
                ''' Comment line '''
                continue
            neighbor_list = []
            
            column = 1
            while column < len(row):
                neighbor_list.append(Neighbor(row[column], (row[column + 1])))
                column += 2
            new_node = DistanceVector(row[0], self, neighbor_list)
            self.nodes.append(new_node)
            self.topodict[row[0]] = new_node

        self.verify_topo()

    def verify_topo(self):
        """Verify that all neighbors in the topology exist."""
        for node in self.nodes:
            try:
                node.verif_neighbors()
            except:
                print("error with neighbors of " + node.name)
                raise


    def run_topo(self):
        """This where most of the action happens. First, we have to prime
        the pump" and send to each neighbor that they are connected.

        Then, in a loop, we go through all of te nodes in topology running

        their intances of Bellman-Ford, passing and reeiving messages until 
        there are no further messages to process. Each loop, print out the
        distances after the loop instance, After the full loop, check to see 
        if we're finished (all queues are empty)."""

        for node in self.nodes:
            node.send_initial_messages()

        done = False
        while done == False:
            for node in self.nodes:
                node.process_BF()
                node.log_distances()

        #Done with a round, Now, we call finish_round() which writes out each
        #entry in log_distances(). By defalut, this will print out alphabetically,
        #which you can turn off so the logfile matches what is printed during
        #log_distances().

            finish_round()

            done = True
            for node in self.nodes:
                if len(node) != 0:
                    done = False
                    break
                # 
                
    #         if row[0] == 'node':
    #         elif row[0] == 'node':
    #             node_name = row[1]
    #             self.topodict[node_name] = Node(node_name, self, [])
    #             self.nodes.append(node_name)
    #         elif row[0] == 'edge':
    #             src, dest, weight = row[1], row[2], float(row[3])
    #             if src in self.topodict and dest in self.topodict:
    #                 neighbor = Neighbor(self.topodict[dest], weight)
    #                 self.topodict[src].links.append(neighbor)
    #                 self.topodict[src].neighbor_names.append(dest)
    #     with open(conf_file, 'r') as file:
    #         reader = csv.reader(file)
    #         for row in reader:
    #             if row[0] == 'node':
    #                 node_name = row[1]
    #                 self.topodict[node_name] = Node(node_name, self, [])
    #                 self.nodes.append(node_name)
    #             elif row[0] == 'edge':
    #                 src, dest, weight = row[1], row[2], float(row[3])
    #                 if src in self.topodict and dest in self.topodict:
    #                     neighbor = Neighbor(self.topodict[dest], weight)
    #                     self.topodict[src].links.append(neighbor)
    #                     self.topodict[src].neighbor_names.append(dest)

    # def load_topology(self):
    #     with open(self.filename, 'r') as file:
    #         reader = csv.reader(file)
    #         for row in reader:
    #             if row[0] == 'node':
    #                 self.nodes.append(row[1])
    #             elif row[0] == 'edge':
    #                 self.edges.append((row[1], row[2], float(row[3])))

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges