# originator.py
import random
from node import Node
from packet import Packet

class Originator(Node):
    def __init__(self, city, symbol_count):
        super().__init__(city, 0)
        self.symbol_count = symbol_count  # Track the number of symbols
        self.ihave_count = 0  # Track the number of ihave packets received
        self.completed = False  # Track if enough symbols have been sent
        self.packet_index = 0  # Track the index of the next packet to send

    def initialize(self):
        self.recipient_ids = [recipient.nodeID for recipient in self.network.recipients]

    def send_packet(self):
        if not self.network or not self.network.recipients:
            return

        # Pick a recipient
        recipient_id = self.recipient_ids[self.packet_index % len(self.recipient_ids)]
        recipient = self.network.recipient_by_id(recipient_id)

        # Pick a symbol index
        symbol_index = self.packet_index % self.symbol_count

        # Create a packet with the selected symbol index
        packet = Packet(source=self, destination=recipient, symbols=[symbol_index])

        # Send the packet through the network
        self.network.send(packet)

        # Increment the packet index
        self.packet_index += 1

    def process_inbox(self):
        while self.inbox:
            packet = self.inbox.pop(0)
            self.ihave_count += 1
            self.network.log(f"Originator received ihave packet from {packet.source.nodeID}")

        # Stop sending packets after receiving five ihave packets
        if self.ihave_count >= 5:
            self.completed = True

    def tick(self):
        self.process_inbox()

        if not self.completed:
            self.send_packet()
