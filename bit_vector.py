class BitVector:
    def __init__(self, length):
        self.length = length
        # Calculate number of 64-bit integers needed
        self.num_words = (length + 63) // 64
        # Initialize array of 64-bit integers
        self.bits = [0] * self.num_words

    def setBit(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Bit index out of range")
        word_index = index // 64
        bit_index = index % 64
        self.bits[word_index] |= (1 << bit_index)

    def setBits(self, indices):
        for index in indices:
            self.setBit(index)

    def valueAt(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Bit index out of range")
        word_index = index // 64
        bit_index = index % 64
        return 1 if (self.bits[word_index] & (1 << bit_index)) else 0

    def inplaceXor(self, other):
        if self.length != other.length:
            raise ValueError("BitVectors must be same length for XOR")
        for i in range(self.num_words):
            self.bits[i] ^= other.bits[i]

    def xor(self, other):
        if self.length != other.length:
            raise ValueError("BitVectors must be same length for XOR")
        result = BitVector(self.length)
        for i in range(self.num_words):
            result.bits[i] = self.bits[i] ^ other.bits[i]
        return result

    def weight(self):
        total = 0
        for word in self.bits:
            # Count bits set in this word using Brian Kernighan's algorithm
            count = 0
            while word:
                word &= (word - 1)
                count += 1
            total += count
        return total

    def __repr__(self):
        bits = [str(self.valueAt(i)) for i in range(self.length)]
        if len(bits) <= 40:
            bit_str = ' '.join(bits)
        else:
            bit_str = ' '.join(bits[:16]) + ' ... ' + ' '.join(bits[-16:])
        return f"BitVector(l={self.length} w={self.weight()} [{bit_str}])"

    def copy(self):
        """Create a deep copy of the BitVector"""
        result = BitVector(self.length)
        result.bits = self.bits.copy()  # Since the bits list contains integers (immutable), a shallow copy is sufficient
        return result


if __name__ == "__main__":
    # Create a bit vector of length 100
    bv = BitVector(100)

    # Set some bits
    bv.setBit(0)
    bv.setBit(99)
    bv.setBits([5, 10, 15])

    # Check values
    print(bv.valueAt(0))  # 1
    print(bv.valueAt(1))  # 0

    # Create another vector and XOR
    bv2 = BitVector(100)
    bv2.setBits([0, 10, 20])

    # In-place XOR
    bv.inplaceXor(bv2)

    # Create new XOR'd vector
    bv3 = bv.xor(bv2)

    # Print representations
    print(bv)
    print(bv2)
    print(bv3)

    # Get weights
    print(bv.weight())
    print(bv2.weight())
    print(bv3.weight())
