import numpy as np
import sympy
from scipy.sparse import random as sparse_random
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr
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
                print(H[:, columns])
                dmin = min(dmin, i)
                break  # No need to check larger combinations
        
        if dmin == i:
            break  # We've found the minimum distance
    
    return dmin

def generate_pretty_good_matrix(k):
    H = np.zeros((k, k), dtype=int)
    

def generate_ldpc_parity_check_matrix(n, m, row_weight=3, col_weight=2):
    """
    Generate a random sparse parity-check matrix H for an LDPC code.
    
    Parameters:
    - n: Codeword length.
    - m: Number of parity bits (rows of H).
    - row_weight: Number of ones per row.
    - col_weight: Number of ones per column.
    
    Returns:
    - H: An m x n sparse parity-check matrix.
    """
    H = np.zeros((m, n), dtype=int)
    
    # Set row and column weights
    for i in range(m):
        ones_positions = np.random.choice(n, row_weight, replace=False)
        H[i, ones_positions] = 1

    for j in range(n):
        # Ensure each column has approximately col_weight ones
        current_col_weight = H[:, j].sum()
        while current_col_weight < col_weight:
            # Randomly pick a row that currently has a 0 in this column
            zero_positions = np.where(H[:, j] == 0)[0]
            row_to_update = np.random.choice(zero_positions)
            H[row_to_update, j] = 1
            current_col_weight += 1
    
    # Convert to sparse matrix format
    return H #csr_matrix(H)

def encode_ldpc_message(H, message):
    """
    Encode a message using the LDPC parity-check matrix H.
    
    Parameters:
    - H: Parity-check matrix (sparse).
    - message: Input message vector of length k.
    
    Returns:
    - codeword: Encoded message vector (length n).
    """
    k = message.size
    n = H.shape[1]
    
    # Initialize codeword with message and zero-padding for parity bits
    codeword = np.zeros(n, dtype=int)
    codeword[:k] = message
    
    # Solve for parity bits to satisfy H * codeword.T = 0
    # Extract parity-check part of H
    A = H[:, k:]  # Parity-check matrix for the parity bits
    b = -H[:, :k].dot(codeword[:k]) % 2  # RHS for the parity bits

    # Solve A * parity_bits = b
    parity_bits = lsqr(A, b)[0] % 2
    parity_bits = np.round(parity_bits).astype(int)

    # Set parity bits in the codeword
    codeword[k:] = parity_bits
    return codeword

# Function to perform Gaussian elimination in Z2
def gaussian_elimination_z2(matrix):
    m, n = matrix.shape
    lead = 0
    for r in range(m):
        if lead >= n:
            return matrix
        i = r
        while matrix[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if n == lead:
                    return matrix
        matrix[i], matrix[r] = matrix[r].copy(), matrix[i].copy()
        for i in range(m):
            if i != r:
                lv = matrix[i][lead]
                matrix[i] = (matrix[i] + lv * matrix[r]) % 2
        lead += 1
    return matrix

# Define parameters for the LDPC code
n = 30  # Codeword length
k = 15   # Message length (half the codeword length)
m = n - k  # Number of parity bits

# Generate the parity-check matrix H with a row weight of 3 and column weight of 2
while True:
    H = generate_ldpc_parity_check_matrix(n, m, row_weight=3, col_weight=2)
    dmin = calculate_dmin(H)
    print("Minimum distance (dmin):", dmin)
    if dmin >= 3:
        break

print("Parity-check matrix H:\n", H)

# Convert H to numpy array if it's not already
H_np = np.array(H)

# Perform Gaussian elimination to get the reduced row echelon form
H_reduced = gaussian_elimination_z2(H_np)

# Convert back to integer type
H_reduced = H_reduced.astype(int)

print("Reduced:\n", H_reduced)

# Generate a random message and encode it using H
message = np.random.randint(0, 2, k)
print("Message:", message)

codeword = encode_ldpc_message(H, message)
print("Encoded codeword:", codeword)