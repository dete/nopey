import numpy as np
import itertools
def calculate_dmin(parity_matrix):
    """
    Calculate the minimum distance (dmin) of a linear code given its parity check matrix.
    
    Args:
    parity_matrix (numpy.ndarray): The parity check matrix H of the code.
    
    Returns:
    int: The minimum distance (dmin) of the code.
    """
    H = np.array(parity_matrix)
    n = H.shape[1]  # Number of columns in H (code length)
    
    dmin = n  # Initialize dmin to the maximum possible value
    
    # Check all possible combinations of columns
    for i in range(1, n + 1):
        for columns in itertools.combinations(range(n), i):
            # Sum the selected columns
            column_sum = np.sum(H[:, columns], axis=1)
            
            # If the sum is all zeros, we've found a codeword
            if np.all(column_sum % 2 == 0):
                print(columns)
                dmin = min(dmin, i)
                break  # No need to check larger combinations
        
        if dmin == i:
            break  # We've found the minimum distance
    
    return dmin

# Example usage:
size = 6

H = np.zeros((size, size*2), dtype=int)

# Set row and column weights
for i in range(size):
    ones_positions = np.random.choice(size*2, size//2, replace=False)
    H[i, ones_positions] = 1

for j in range(size*2):
    # Ensure each column has approximately col_weight ones
    current_col_weight = H[:, j].sum()
    while current_col_weight < size//2:
        # Randomly pick a row that currently has a 0 in this column
        zero_positions = np.where(H[:, j] == 0)[0]
        row_to_update = np.random.choice(zero_positions)
        H[row_to_update, j] = 1
        current_col_weight += 1

print(H)
    # [[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    #           [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    #           [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1],
    #           [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1],
    #           [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    #           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0]])
print(calculate_dmin(H))
