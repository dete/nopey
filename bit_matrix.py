from bit_vector import BitVector

class BitMatrix:
    def __init__(self, width):
        self.width = width
        self.rows = []

    def identity(self):
        if len(self.rows) != 0:
            raise ValueError("Can only create identity matrix from empty matrix")
        
        for i in range(self.width):
            row = BitVector(self.width)
            row.setBit(i)
            self.rows.append(row)
        return self

    def shape(self):
        return (len(self.rows), self.width)

    def append(self, row):
        if not isinstance(row, BitVector):
            raise TypeError("Row must be a BitVector")
        if row.length != self.width:
            raise ValueError(f"Row length {row.length} does not match matrix width {self.width}")
        self.rows.append(row)

    def _find_pivot(self, col, start_row):
        """Helper method to find the first row with a 1 in the given column"""
        for i in range(start_row, len(self.rows)):
            if self.rows[i].valueAt(col) == 1:
                return i
        return None

    def copy(self):
        """Create a deep copy of the matrix"""
        result = BitMatrix(self.width)
        for row in self.rows:
            result.append(row.copy())  # Use BitVector's copy method
        return result

    def rank(self):
        if len(self.rows) == 0:
            return 0

        # Create a copy of the matrix to perform non-destructive Gaussian elimination
        matrix = self.copy()
        rank = 0
        row = 0
        
        for col in range(self.width):
            # Find pivot
            pivot_row = matrix._find_pivot(col, row)
            
            if pivot_row is not None:
                # Swap rows if necessary
                if pivot_row != row:
                    matrix.rows[row], matrix.rows[pivot_row] = matrix.rows[pivot_row], matrix.rows[row]
                
                # Eliminate column entries
                for i in range(len(matrix.rows)):
                    if i != row and matrix.rows[i].valueAt(col) == 1:
                        matrix.rows[i].inplaceXor(matrix.rows[row])
                
                rank += 1
                row += 1
                
                if row == len(matrix.rows):
                    break

        return rank

    def inverse(self):
        if len(self.rows) != self.width:
            raise ValueError("Matrix must be square to have an inverse")

        # Create working copy of this matrix
        work_matrix = self.copy()
        
        # Create identity matrix of same size
        result = BitMatrix(self.width)
        result.identity()

        # Perform Gaussian elimination
        for col in range(self.width):
            pivot_row = work_matrix._find_pivot(col, col)
            
            if pivot_row is None:
                raise ValueError("Matrix is not invertible")
            
            # Swap rows if necessary
            if pivot_row != col:
                work_matrix.rows[col], work_matrix.rows[pivot_row] = work_matrix.rows[pivot_row], work_matrix.rows[col]
                result.rows[col], result.rows[pivot_row] = result.rows[pivot_row], result.rows[col]
            
            # Eliminate column entries
            for row in range(self.width):
                if row != col and work_matrix.rows[row].valueAt(col) == 1:
                    work_matrix.rows[row].inplaceXor(work_matrix.rows[col])
                    result.rows[row].inplaceXor(result.rows[col])

        # Verify that we have an identity matrix
        for i in range(self.width):
            for j in range(self.width):
                if work_matrix.rows[i].valueAt(j) != (1 if i == j else 0):
                    raise ValueError("Matrix is not invertible")

        return result

    def __repr__(self):
        shape_str = f"BitMatrix(shape={self.shape()})"
        if len(self.rows) == 0:
            return shape_str
        
        # Format each row's bits like BitVector does, but without the BitVector wrapper text
        row_bits = []
        for row in self.rows:
            bits = [str(row.valueAt(i)) for i in range(row.length)]
            if len(bits) <= 40:
                bit_str = ' '.join(bits)
            else:
                bit_str = ' '.join(bits[:16]) + ' ... ' + ' '.join(bits[-16:])
            row_bits.append(bit_str)
            
        rows_str = '\n'.join(row_bits)
        return f"{shape_str}\n{rows_str}"

if __name__ == "__main__":
    # Create a 3x3 identity matrix
    m = BitMatrix(3)
    m.identity()
    print("Identity matrix:")
    print(m)

    # Create a custom matrix
    m2 = BitMatrix(3)
    row1 = BitVector(3)
    row1.setBits([0, 1])
    row2 = BitVector(3)
    row2.setBits([1, 2])
    row3 = BitVector(3)
    row3.setBits([0, 1, 2])

    m2.append(row1)
    m2.append(row2)
    m2.append(row3)

    print("\nCustom matrix:")
    print(m2)

    print("\nRank:", m2.rank())

    try:
        inv = m2.inverse()
        print("\nInverse:")
        print(inv)
        
        # Verify inverse
        print("\nOriginal matrix shape:", m2.shape())
        print("Inverse matrix shape:", inv.shape())
    except ValueError as e:
        print("Matrix is not invertible:", e)
