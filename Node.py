class Neighbor(object):
    def __init__(self, node, weight):
        self.node = node
        self.weight = weight

    def __repr__(self):
        return f"Neighbor(node={self.node}, weight={self.weight})"
    
    def get_name(self):
        if isinstance(self.node, Node):
            return self.node.name
        return str(self.node)
    
    def get_weight(self):
        return self.weight


class Node(object):
    def __init__(self, name, topolink, neighbors):
        self.name = name
        self.topology = topolink
        self.links = neighbors
        self.neighbor_names = []
        self.messages = []
        
        for neighbor in neighbors:
            self.neighbor_names.append(neighbor.get_name())

    def get_neighbor_weights(self, neighbor_name):
        for neighbor in self.links:
            if neighbor.get_name() == neighbor_name:
                return neighbor.get_weight()
        return "Node Not found"
    
    def __len__(self):
        return len(self.links)
    
    def __str__(self):
        retstr = self.name + " has neighbors: "
        for neighbor in self.links:
            retstr += retstr + neighbor.get_name() + neighbor.get_weight() + ", "
        return retstr[:-2]  # Remove the last comma and space
    
    def __repr__(self):
        return self.__str__()
    
    def verify_neighbors(self):
        for neighbor in self.links:
            if neighbor.get_name() not in self.neighbor_names:
                raise Exception(neighbor.get_name() + " is not a valid neighbor for " + self.name)

    def send_msg(self, msg, dest):
        """Send a message to a neighbor node."""
        if dest not in self.neighbor_names:
            raise Exception(f"Neighbor " + dest + " not part of neighbors of " + self.name)
        self.topology.topodict[dest].queue_msg(msg)


    def queue_msg(self, msg):
        """Queue a message to be processed later."""
        self.messages.append(msg)

    def add_neighbor(self, neighbor):
        self.links.append(neighbor)
        if isinstance(neighbor, Neighbor):
            self.neighbor_names.append(neighbor.get_name())
    
    def get_neighbors(self):
        return self.links

    def get_name(self):
        return self.name