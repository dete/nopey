class Codeword:
    def __init__(self, source, destination, symbols):
        self.source = source  # Reference to a Node object or None
        self.destination = destination  # Reference to a Node object
        self.symbols = symbols  # Array of integer symbolIDs

    def __repr__(self):
        from recipient import Recipient
        source_id = self.source.nodeID if isinstance(self.source, Recipient) else "Orig"
        destination_id = self.destination.nodeID
        return f"Codeword(source={source_id}, destination={destination_id}, symbols={self.symbols})"

    # ... additional methods if needed ...
