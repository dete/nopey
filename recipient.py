# recipient.py
from node import Node
import config
from codeword import Codeword  # Updated import
import random

class Recipient(Node):
    def __init__(self, city, nodeID, total_symbols):
        super().__init__(city, nodeID)
        self.total_symbols = total_symbols
        self.seen_symbols = set()  # Track seen symbols
        self.completed = False  # Flag to track if completion codeword has been sent
        self.codewords_to_forward = []

    def initialize(self):
        pass

    def process_codeword(self, codeword):
        if not self.completed:
            previously_seen = len(self.seen_symbols)

            for symbol in codeword.symbols:
                self.seen_symbols.add(symbol)

            # If we've seen all the symbols before, don't forward the codeword
            if previously_seen == len(self.seen_symbols):
                return

            if codeword.source == self.network.originator:
                my_index = self.network.recipients.index(self)

                for i in range(len(self.network.recipients)):
                    recipient = self.network.recipients[i % len(self.network.recipients)]
                    downstream_codeword = Codeword(source=self, destination=recipient, symbols=codeword.symbols)
                    self.codewords_to_forward.append(downstream_codeword)

            # Check if all symbols have been seen and completion codeword hasn't been sent
            if len(self.seen_symbols) == self.total_symbols:
                self.completed = True  # Set the flag to indicate completion codeword has been sent

                # Send a codeword with an empty symbol list back to the originator
                response_codeword = Codeword(source=self, destination=self.network.originator, symbols=[])
                self.network.send(response_codeword)
                self.network.log(f"Node {self.nodeID} received all symbols")

    def tick(self):
        # Customizable logic for processing received codewords
        if self.inbox:
            codeword = self.inbox.pop(0)
            self.process_codeword(codeword)
        else:
            if self.codewords_to_forward:
                codeword = self.codewords_to_forward.pop(0)
                self.network.send(codeword)
