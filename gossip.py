from strategy import Strategy
from locations import get_latency
import random
import math

class GossipStrategy(Strategy):
    def __init__(self, network, k, degree=4):
        super().__init__(network, k)
        self.degree = degree
        self.neighbors = {n: [] for n in network.recipients}
        self.has_forwarded = False

    def add_closest_neighbors(self, count, network):
        for node in network.recipients:
            current_neighbors = self.neighbors[node]
            possible_neighbors = [n for n in network.recipients if n != node and n not in current_neighbors]
            self.neighbors[node].extend(sorted(possible_neighbors, key=lambda x: get_latency(node.city, x.city))[:count])

    def add_random_neighbors(self, count, network):
        for node in network.recipients:
            current_neighbors = self.neighbors[node]
            possible_neighbors = [n for n in network.recipients if n != node and n not in current_neighbors]
            new_neighbors = random.sample(possible_neighbors, count)
            self.neighbors[node].extend(new_neighbors)

    def get_recipients(self, sender_index, codeword_index):
        if not self.has_forwarded:
            self.has_forwarded = True

            # Return all neighbors except the sender
            if sender_index is not None:
                return [n for n in self.neighbors if n != sender_index]
            else:
                return self.neighbors
        else:
            return []
    

class GreedyGossipStrategy(GossipStrategy):
    def __init__(self, network, k, degree=4):
        super().__init__(network, k, degree)
        self.add_closest_neighbors(degree, network)

class RandomGossipStrategy(GossipStrategy):
    def __init__(self, network, k, degree=4):
        super().__init__(network, k, degree)
        self.add_random_neighbors(degree, network)

class HalfGreedyGossipStrategy(GossipStrategy):
    def __init__(self, network, k, degree=4):
        super().__init__(network, k, degree)
        self.add_closest_neighbors(math.floor(degree / 2), network)
        self.add_random_neighbors(math.ceil(degree / 2), network)

if __name__ == "__main__":
    from network import Network
    from originator import Originator
    from recipient import Recipient
    from locations import *

    originator = Originator(get_random_location(), 1)
    recipients = [Recipient(get_random_location(), i+1, 1) for i in range(100)]

    network = Network(originator, recipients)
    network.initialize()

    # Test GreedyGossipStrategy
    greedyStrat = GreedyGossipStrategy(network, k=5, degree=3)
    for node in recipients:
        neighbors = greedyStrat.neighbors[node]
        print(f"Node {node.nodeID} neighbors (Greedy):", [n.nodeID for n in neighbors])
        print(f"Latencies: {[get_latency(node.city, n.city) for n in neighbors]}")
        assert len(neighbors) == 3, "Should have exactly 3 neighbors"
        assert node not in neighbors, "Node shouldn't be its own neighbor"

    # Test RandomGossipStrategy 
    randomStrat = RandomGossipStrategy(network, k=5, degree=3)
    for node in recipients:
        neighbors = randomStrat.neighbors[node]
        print(f"Node {node.nodeID} neighbors (Random):", [n.nodeID for n in neighbors])
        print(f"Latencies: {[get_latency(node.city, n.city) for n in neighbors]}")
        assert len(neighbors) == 3, "Should have exactly 3 neighbors"
        assert node not in neighbors, "Node shouldn't be its own neighbor"

    # Test HalfGreedyGossipStrategy
    halfStrat = HalfGreedyGossipStrategy(network, k=5, degree=4)
    for node in recipients:
        neighbors = halfStrat.neighbors[node]
        print(f"Node {node.nodeID} neighbors (HalfGreedy):", [n.nodeID for n in neighbors])
        print(f"Latencies: {[get_latency(node.city, n.city) for n in neighbors]}")
        assert len(neighbors) == 4, "Should have exactly 4 neighbors"
        assert node not in neighbors, "Node shouldn't be its own neighbor"

    print("All tests passed!")
