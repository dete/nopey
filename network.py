# network.py
from locations import *
import config

class Network:
    def __init__(self, originator, recipients):
        self.originator = originator
        self.recipients = recipients
        self.recipient_lookup = {recipient.nodeID: recipient for recipient in recipients}
        self.packets_in_transit = []  # List to store packets and their delivery tick
        self.packet_counts = {recipient: 0 for recipient in recipients}  # Track packet counts per recipient
        self.tick_count = 0  # Initialize tick count
        self.total_packets = 0

        # Set the network reference for the originator and recipients
        self.originator.set_network(self)
        for recipient in self.recipients:
            recipient.set_network(self)

    def initialize(self):
        for node in [self.originator] + self.recipients:
            node.initialize()

    def send(self, packet):
        # Look up the latency between the source and destination
        latency = latency_table[packet.source.city][packet.destination.city]

        # Calculate the delivery tick
        delivery_tick = self.tick_count + latency

        # Insert the packet into the sorted list
        self.insert_packet(packet, delivery_tick)

        # Increment the packet count for the destination if it's a recipient
        if packet.destination in self.packet_counts:
            self.packet_counts[packet.destination] += 1

        self.total_packets += 1
    
    def insert_packet(self, packet, delivery_tick):
        # Binary search to find the correct position to insert the packet
        left, right = 0, len(self.packets_in_transit)
        while left < right:
            mid = (left + right) // 2
            if self.packets_in_transit[mid][1] > delivery_tick:
                left = mid + 1
            else:
                right = mid
        self.packets_in_transit.insert(left, (packet, delivery_tick))
    
    def tick(self):
        self.tick_count += 1  # Increment tick count

        # Deliver packets scheduled for this tick
        while self.packets_in_transit and self.packets_in_transit[-1][1] <= self.tick_count:
            packet, _ = self.packets_in_transit.pop()
            packet.destination.receive_message(packet)
            # Decrement the packet count for the destination if it's a recipient
            if packet.destination in self.packet_counts:
                self.packet_counts[packet.destination] -= 1

        self.originator.tick()
        for recipient in self.recipients:
            recipient.tick()
        
        #self.log(f"Packet counts: {[f'{node.nodeID}: {count}' for node, count in self.packet_counts.items()]}")

    def active(self):
        # Check if the originator's complete flag is set
        if not self.originator.completed:
            return True

        # Check if there are any packets in transit
        if self.packets_in_transit:
            return True

        # Check if there are any packets in any node's inbox
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
                f"packets_in_transit={len(self.packets_in_transit)}, "
                f"originator_completed={self.originator.completed}, "
                f"recipients_completed={[recipient.completed for recipient in self.recipients]}, "
                f"total_packets={self.total_packets})")
