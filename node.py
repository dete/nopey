class Node:
    def __init__(self, city, nodeID):
        self.city = city
        self.nodeID = nodeID  # Move nodeID to Node class
        self.inbox = []
        self.network = None  # New member variable for Network instance

    def receive_message(self, packet):
        self.inbox.append(packet)

    def tick(self):
        # Define behavior for each tick
        pass

    def initialize(self):
        pass

    def set_network(self, network):
        self.network = network  # Mutator function to set the Network instance
