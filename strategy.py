class Strategy:
    def __init__(self, network, k):
        """Initialize Strategy with network and k symbols."""
        self.network = network
        self.n = len(network.recipients)
        self.k = k
    
    def get_recipients(self, sender_index, codeword_index):
        """
        Get list of recipients for a given sender and codeword index.
        To be implemented by subclasses.
        """
        raise NotImplementedError

