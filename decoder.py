import numpy as np

class Decoder:
    def __init__(self, total_symbols):
        self.total_symbols = total_symbols
        self.vectors = []


    def _gaussian_elimination_z2(self, matrix):
        binary_matrix = matrix.astype(np.int8) % 2
        rows, cols = binary_matrix.shape
        rank = 0
        lead = 0

        for r in range(rows):
            if lead >= cols:
                break
                
            # Find pivot
            i = r
            while i < rows and binary_matrix[i][lead] == 0:
                i += 1
                
            if i == rows:
                lead += 1
                continue
                
            # Swap rows
            if i != r:
                binary_matrix[r], binary_matrix[i] = binary_matrix[i].copy(), binary_matrix[r].copy()
                
            # Eliminate column entries
            for i in range(rows):
                if i != r and binary_matrix[i][lead] == 1:
                    binary_matrix[i] = (binary_matrix[i] + binary_matrix[r]) % 2
                    
            lead += 1
            rank += 1

        # if rank == cols or rows > cols*2:
        #     print(matrix)
        #     print(binary_matrix)
        #     exit()

        return rank

    def process_codeword(self, codeword):
        # Create vector of zeros with 1s at symbol positions
        vector = np.zeros(self.total_symbols, dtype=np.int8)
        for symbol in codeword.symbols:
            vector[symbol] = 1
            
        # Add vector as new row
        if not any(np.array_equal(vector, existing_vector) for existing_vector in self.vectors):
            self.vectors.append(vector)
        
        # Convert to numpy array and check rank
        matrix = np.array(self.vectors)
        rank = self._gaussian_elimination_z2(matrix)
        
        if rank == self.total_symbols:
            print(f"Rank: {rank}/{len(self.vectors)} ({int(((len(self.vectors)/rank) - 1) * 100)}%)")

        # Return true if rank equals dimension (forms basis)
        return rank == self.total_symbols
