from bit_matrix import BitMatrix
from bit_vector import BitVector

class Decoder:
    def __init__(self, total_symbols):
        self.total_symbols = total_symbols
        self.matrix = BitMatrix(total_symbols)

    def process_codeword(self, codeword):
        # Create BitVector from codeword symbols
        vector = BitVector(self.total_symbols)
        vector.setBits(codeword.symbols)
        
        # Check if this vector is linearly independent
        # by seeing if adding it increases the rank
#        old_rank = self.matrix.rank()
        self.matrix.append(vector)
        new_rank = self.matrix.rank()
        
        # If rank didn't increase, this vector was dependent
        # if new_rank == old_rank:
        #     # Remove the dependent vector
        #     self.matrix.rows.pop()
        
        if new_rank == self.total_symbols:
            print(f"Rank: {new_rank}/{len(self.matrix.rows)} ({int(((len(self.matrix.rows)/new_rank) - 1) * 100)}%)")

        # Return true if rank equals dimension (forms basis)
        return new_rank == self.total_symbols
