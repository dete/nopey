# network.py
from locations import *
import config

class Network:
    def __init__(self, originator, recipients):
        self.originator = originator
        self.recipients = recipients
        self.recipient_lookup = {recipient.nodeID: recipient for recipient in recipients}
        self.codewords_in_transit = []
        self.codeword_counts = {recipient: 0 for recipient in recipients}
        self.tick_count = 0  # Initialize tick count
        self.total_codewords = 0  #

        # Set the network reference for the originator and recipients
        self.originator.set_network(self)
        for recipient in self.recipients:
            recipient.set_network(self)

    def initialize(self):
        for node in [self.originator] + self.recipients:
            node.initialize()

    def send(self, codeword):  # Renamed parameter
        # Look up the latency between the source and destination
        latency = latency_table[codeword.source.city][codeword.destination.city]

        # Calculate the delivery tick
        delivery_tick = self.tick_count + latency

        # Insert the codeword into the sorted list
        self.insert_codeword(codeword, delivery_tick)  # Renamed method call

        # Increment the codeword count for the destination if it's a recipient
        if codeword.destination in self.codeword_counts:
            self.codeword_counts[codeword.destination] += 1

        self.total_codewords += 1
    
    def insert_codeword(self, codeword, delivery_tick):
        # Binary search to find the correct position to insert the codeword
        left, right = 0, len(self.codewords_in_transit)
        while left < right:
            mid = (left + right) // 2
            if self.codewords_in_transit[mid][1] > delivery_tick:
                left = mid + 1
            else:
                right = mid
        self.codewords_in_transit.insert(left, (codeword, delivery_tick))
    
    def tick(self):
        self.tick_count += 1  # Increment tick count

        # Deliver codewords scheduled for this tick
        while self.codewords_in_transit and self.codewords_in_transit[-1][1] <= self.tick_count:
            codeword, _ = self.codewords_in_transit.pop()
            codeword.destination.receive_codeword(codeword)
            # Decrement the codeword count for the destination if it's a recipient
            if codeword.destination in self.codeword_counts:
                self.codeword_counts[codeword.destination] -= 1

        self.originator.tick()
        for recipient in self.recipients:
            recipient.tick()

    def active(self):
        # Check if the originator's complete flag is set
        if not self.originator.completed:
            return True

        # Check if there are any codewords in transit
        if self.codewords_in_transit:
            return True

        # Check if there are any codewords in any node's inbox
        for node in [self.originator] + self.recipients:
            if node.inbox:
                return True

        return False

    def recipient_by_id(self, nodeID):
        return self.recipient_lookup.get(nodeID, None)

    def log(self, message):
        if config.VERBOSE:
            print(f"{self.tick_count}: {message}")

    def __repr__(self):
        return (f"Network(tick_count={self.tick_count}, "
                f"codewords_in_transit={len(self.codewords_in_transit)}, "
                f"originator_completed={self.originator.completed}, "
                f"recipients_completed={[recipient.completed for recipient in self.recipients]}, "
                f"total_codewords={self.total_codewords})")
