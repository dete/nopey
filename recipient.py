# recipient.py
from node import Node
import config
from codeword import Codeword  # Updated import
from decoder import Decoder
import random

class Recipient(Node):
    def __init__(self, city, nodeID, total_symbols):
        super().__init__(city, nodeID)
        self.total_symbols = total_symbols
        self.decoder = Decoder(total_symbols)
        self.completed = False  # Flag to track if completion codeword has been sent
        self.codewords_to_forward = []

    def initialize(self):
        pass

    def process_codeword(self, codeword):
        if not self.completed:

            # Queue up codewords to forward to downstream recipients
            if codeword.source == self.network.originator:
                my_index = self.network.recipients.index(self)

                for i in range(len(self.network.recipients)-1):
                    recipient = self.network.recipients[(my_index + i) % len(self.network.recipients)]
                    downstream_codeword = Codeword(source=self, destination=recipient, symbols=codeword.symbols)
                    self.codewords_to_forward.append(downstream_codeword)

            # Check if all symbols have been seen and send a response codeword to tell the originator I'm done
            self.completed = self.decoder.process_codeword(codeword)
            if self.completed:
                # Send a codeword with an empty symbol list back to the originator
                response_codeword = Codeword(source=self, destination=self.network.originator, symbols=[])
                self.network.send(response_codeword)
                self.network.log(f"Node {self.nodeID} complete after {self.decoder.matrix.shape()[0]} codewords")

    def tick(self):
        # Process an incoming codeword first. If there are none, forward a single codeword
        if self.inbox:
            codeword = self.inbox.pop(0)
            self.process_codeword(codeword)
        else:
            if self.codewords_to_forward:
                codeword = self.codewords_to_forward.pop(0)
                self.network.send(codeword)
