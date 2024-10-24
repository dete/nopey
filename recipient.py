# recipient.py
from node import Node
import config
from packet import Packet
import random

class Recipient(Node):
    def __init__(self, city, nodeID, total_symbols):
        super().__init__(city, nodeID)
        self.total_symbols = total_symbols
        self.seen_symbols = set()  # Track seen symbols
        self.completed = False  # Flag to track if completion packet has been sent

    def initialize(self):
        pass

    def process_packet(self, packet):
        if not self.completed:
            # Forward this packet to the next recipient in the network (wrapping around if at the end)
            current_index = self.network.recipients.index(self)
            next_index = (current_index + 1) % len(self.network.recipients)
            recipient = self.network.recipients[next_index]
            downstream_packet = Packet(source=self, destination=recipient, symbols=packet.symbols)
            self.network.send(downstream_packet)

            for symbol in packet.symbols:
                self.seen_symbols.add(symbol)

            # Check if all symbols have been seen and completion packet hasn't been sent
            if len(self.seen_symbols) == self.total_symbols:
                self.completed = True  # Set the flag to indicate completion packet has been sent

                # Send a packet with an empty symbol list back to the originator
                response_packet = Packet(source=self, destination=self.network.originator, symbols=[])
                self.network.send(response_packet)
                self.network.log(f"Node {self.nodeID} received all symbols")

    def tick(self):
        # Customizable logic for processing received packets
        if self.inbox:
            packet = self.inbox.pop(0)
            self.process_packet(packet)
            
