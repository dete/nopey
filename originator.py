# originator.py
import random
from node import Node
from codeword import Codeword  # Updated import

class Originator(Node):
    def __init__(self, city, symbol_count):
        super().__init__(city, 0)
        self.symbol_count = symbol_count  # Track the number of symbols
        self.ihave_count = 0  # Track the number of ihave codewords received
        self.completed = False  # Track if enough symbols have been sent
        self.codeword_index = 0

    def initialize(self):
        self.recipient_ids = [recipient.nodeID for recipient in self.network.recipients]

    def send_codeword(self):
        if not self.network or not self.network.recipients:
            return

        # Pick a recipient
        recipient_id = self.recipient_ids[(self.codeword_index) % len(self.recipient_ids)]
        recipient = self.network.recipient_by_id(recipient_id)

        # Create a random set of symbols if not already created
        symbol_count = random.randint(1, self.symbol_count)
        symbol_set = random.sample(range(self.symbol_count), symbol_count)

        # Create a codeword with the selected symbol index
        codeword = Codeword(source=self, destination=recipient, symbols=symbol_set)

        # Send the codeword through the network
        self.network.send(codeword)

        # Increment the codeword index
        self.codeword_index += 1

        if self.codeword_index > self.symbol_count * 1.2:
            self.completed = True

    def process_inbox(self):
        while self.inbox:
            codeword = self.inbox.pop(0)
            self.ihave_count += 1
            self.network.log(f"Originator received ihave codeword from {codeword.source.nodeID}")

        # Stop sending codewords after receiving five ihave codewords
        if self.ihave_count >= 5:
            self.completed = True

    def tick(self):
        self.process_inbox()

        if not self.completed:
            self.send_codeword()  # Renamed method call
