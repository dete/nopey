# fanout.py
import math
from strategy import Strategy
from enum import Enum

class FanoutType(Enum):
    SEND_ALL = 1
    SEND_ONE = 2 
    FANOUT = 3

class FanoutStrategy(Strategy):
    def __init__(self, network, k):
        """
        Initialize Fanout with n recipients and k symbols.
        Creates a list of integers x < n where GCD(x,n) = 1
        """
        def gcd(a, b):
            """Calculate the Greatest Common Divisor of a and b using Euclidean algorithm."""
            while b:
                a, b = b, a % b
            return a

        super().__init__(network, k)
        self.first_recipient_count = 0
        self.second_recipient_count = 0

        # Total number of codewords to be sent, to all recipients
        total_sent_codewords = self.n * self.k

        if total_sent_codewords <= 200:
            self.first_recipient_count = total_sent_codewords
            self.second_recipient_count = 0
            self.type = FanoutType.SEND_ALL
        elif self.k >= self.n:
            self.first_recipient_count = self.k
            self.second_recipient_count = 0
            self.type = FanoutType.SEND_ONE
        else:
            self.first_recipient_count = math.ceil(math.sqrt(self.n)/self.k)
            self.second_recipient_count = math.ceil(self.n / self.first_recipient_count)
            self.type = FanoutType.FANOUT

            # Generate list of coprime numbers less than n
            self.coprimes = [x for x in range(1, self.n) if gcd(x, self.n) == 1]

    def get_recipients(self, sender_index, codeword_index):
        if sender_index == -1:
            return self.get_first_recipients(codeword_index)
        else:
            return self.get_second_recipients(sender_index, codeword_index)

    def get_first_recipients(self, codeword_index):
        if self.type == FanoutType.SEND_ALL:
            return [x for x in range(self.n)]
        elif self.type == FanoutType.SEND_ONE:
            return [codeword_index % self.n]
        else:
            stride = self.coprimes[codeword_index*7 % len(self.coprimes)]
            return [(codeword_index + x*stride*self.second_recipient_count) % self.n for x in range(self.first_recipient_count)]

    def get_second_recipients(self, recipient_index, codeword_index):
        if self.type == FanoutType.SEND_ALL:
            return []
        elif self.type == FanoutType.SEND_ONE:
            return [x for x in range(self.n) if x != recipient_index]
        else:
            stride = self.coprimes[codeword_index*7 % len(self.coprimes)]
            return [(recipient_index + x*stride) % self.n for x in range(1, self.second_recipient_count)]

if __name__ == "__main__":
    n = 100
    k = 10
    fanout = FanoutStrategy(n, k)
    print(fanout.type)

    # Calculate codewords sent by each recipient
    codewords_sent = [0] * n
    sent_codewords = 0
    
    # For each codeword
    for codeword_index in range(k):
        # Get first recipients
        first_recipients = fanout.get_first_recipients(codeword_index)
        sent_codewords += len(first_recipients)

        # First recipients forward to their second recipients
        for recipient in first_recipients:
            second_recipients = fanout.get_second_recipients(recipient, codeword_index)
            codewords_sent[recipient] += len(second_recipients)
    
    # Print stats about forwarding
    total_forwards = sum(codewords_sent)
    avg_forwards = total_forwards / n
    max_forwards = max(codewords_sent)
    min_forwards = min(codewords_sent)
    
    print(f"Origin sent: {sent_codewords}")
    print(f"Average forwards: {avg_forwards:.1f}")
    print(f"Max forwards: {max_forwards}")
    print(f"Min forwards: {min_forwards}")
    # print(f"Nodes with most forwards: {[i for i,v in enumerate(codewords_sent) if v == max_forwards]}")

    # Track which nodes have been included
    for codeword_index in range(k):
        print(f"Codeword {codeword_index}:")
        print("Stride:", fanout.coprimes[codeword_index % len(fanout.coprimes)])
        
        # Get first recipients for this codeword
        first_recipients = fanout.get_first_recipients(codeword_index)
        print(f"First recipients: {first_recipients}")
        
        # Track which nodes are included
        included_nodes = set(first_recipients)
        
        # For each first recipient, get their second recipients
        for recipient in first_recipients:
            second_recipients = fanout.get_second_recipients(recipient, codeword_index)
            print(f"  {recipient} -> {second_recipients}")
            
            # Add second recipients to tracking set
            included_nodes.update(second_recipients)
        
        # Check coverage and duplicates
        missing_nodes = set(range(fanout.n)) - included_nodes
        if missing_nodes:
            print(f"Missing nodes: {sorted(list(missing_nodes))}")
            
        # Find nodes included multiple times
        all_recipients = first_recipients + [r for f in first_recipients for r in fanout.get_second_recipients(f, codeword_index)]
        duplicates = {x for x in all_recipients if all_recipients.count(x) > 1}
        if duplicates:
            print(f"Nodes included multiple times: {sorted(list(duplicates))}")
