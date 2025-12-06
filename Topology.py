from Node import Node, Neighbor
import csv


class Topology(object):
    def __init__(self, conf_file):
        """Initialize the topology with a configuration file."""
        self.topodict = {}
        self.nodes = []
        self.topo__from__conf_file(conf_file)

    def topo__from__conf_file(self, conf_file):
        """Load the topology from a configuration file."""
        with open(conf_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 0:
                    # Empty row
                    continue
                if row[0].startswith('#'):
                    # Comment line
                    continue
                
                if row[0] == 'node':
                    node_name = row[1]
                    self.topodict[node_name] = Node(node_name, self, [])
                    self.nodes.append(node_name)
                elif row[0] == 'edge':
                    src, dest, weight = row[1], row[2], float(row[3])
                    if src in self.topodict and dest in self.topodict:
                        neighbor = Neighbor(self.topodict[dest], weight)
                        self.topodict[src].links.append(neighbor)
                        self.topodict[src].neighbor_names.append(dest)

    def get_nodes(self):
        return self.nodes