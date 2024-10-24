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
        self.packets_to_forward = []

    def initialize(self):
        pass

    def process_packet(self, packet):
        if not self.completed:
            previously_seen = len(self.seen_symbols)

            for symbol in packet.symbols:
                self.seen_symbols.add(symbol)

            # If we've seen all the symbols before, don't forward the packet
            if previously_seen == len(self.seen_symbols):
                return

            if packet.source == self.network.originator:
                my_index = self.network.recipients.index(self)

                for i in range(len(self.network.recipients)):
                    recipient = self.network.recipients[i % len(self.network.recipients)]
                    downstream_packet = Packet(source=self, destination=recipient, symbols=packet.symbols)
                    self.packets_to_forward.append(downstream_packet)

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
        else:
            if self.packets_to_forward:
                packet = self.packets_to_forward.pop(0)
                self.network.send(packet)
