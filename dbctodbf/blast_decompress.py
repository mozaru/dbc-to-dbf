"""
BLAST decompressor - Python version
Originally based on blast.c by Mark Adler (zlib license)
Ported and extended by Mozar Silva - 2025

Licensed under the zlib License (see LICENSE file for details).
"""

class BlastState:
    __MAXWIN__ = 4096

    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0
        self.bitbuf = 0
        self.bitcnt = 0
        self.output = bytearray()
        self.window = bytearray(BlastState.__MAXWIN__)
        self.next = 0
        self.first = True

    def bits(self, need: int) -> int:
        val = self.bitbuf
        while self.bitcnt < need:
            if self.pos >= len(self.data):
                raise EOFError("Not enough input data")
            val |= self.data[self.pos] << self.bitcnt
            self.bitcnt += 8
            self.pos += 1

        self.bitbuf = val >> need
        self.bitcnt -= need
        return val & ((1 << need) - 1)

class Huffman:
    __MAXBITS__ = 13


    def __init__(self, rep: list[int]):
        self.count = [0] * (Huffman.__MAXBITS__ + 1)
        self.symbol = []

        length = []
        for val in rep:
            count = (val >> 4) + 1
            bitlen = val & 0x0F
            length.extend([bitlen] * count)

        for l in length:
            self.count[l] += 1

        if self.count[0] == len(length):
            raise ValueError("Invalid Huffman code [no codes]")

        count = 1
        for val in range(1, Huffman.__MAXBITS__ + 1):
            count <<= 1
            count -= self.count[val]
            if count < 0:
                raise ValueError("Invalid Huffman code [over-subscribed]")

        offs = [0] * (Huffman.__MAXBITS__ + 1)
        for i in range(1, Huffman.__MAXBITS__):
            offs[i + 1] = offs[i] + self.count[i]

        self.symbol = [0] * len(length)
        for i, l in enumerate(length):
            if l != 0:
                self.symbol[offs[l]] = i
                offs[l] += 1

    def decode(self, state: BlastState) -> int:
        code = 0
        first = 0
        index = 0
        for length in range(1, Huffman.__MAXBITS__ + 1):
            bit = state.bits(1)
            code = (code << 1) | (bit ^ 1)  # invertido, como no blast.c
            count = self.count[length]
            if code < first + count:
                return self.symbol[index + (code - first)]
            index += count
            first = (first + count) << 1
        raise ValueError("Invalid Huffman code")

class BlastDecompress:
    # Tabelas fixas do algoritmo
    _LITLEN_ = [
    11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8,
    9, 7, 6, 7, 8, 7, 6, 55, 8, 23, 24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5,
    7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9, 8, 25, 11, 8, 11, 9, 12,
    8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27,
    44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45, 12, 61, 12, 45,
    44, 173 ]
    _LENLEN_ = [2, 35, 36, 53, 38, 23]
    _DISTLEN_ = [2, 20, 53, 230, 247, 151, 248]
    _BASE_ = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
    _EXTRA_ = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self):
        self.__litcode = Huffman(BlastDecompress._LITLEN_)
        self.__lencode = Huffman(BlastDecompress._LENLEN_)
        self.__distcode = Huffman(BlastDecompress._DISTLEN_)

    def decompress(self, compressed_data: bytearray) -> bytearray:
        s = BlastState(compressed_data)
        MAXWIN = len(s.window)
        # Cabeçalho
        lit = s.bits(8)
        if lit > 1:
            raise ValueError("Invalid literal flag")
        dict_ = s.bits(8)
        if dict_ < 4 or dict_ > 6:
            raise ValueError("Invalid dictionary size")

        while True:
            if s.bits(1):
                # Sequência comprimida
                symbol = self.__lencode.decode(s)
                length = BlastDecompress._BASE_[symbol] + s.bits(BlastDecompress._EXTRA_[symbol])
                if length == 519:
                    break  # código de fim

                distbits = 2 if length == 2 else dict_
                dist = (self.__distcode.decode(s) << distbits) + s.bits(distbits) + 1

                if s.first and dist > s.next:
                    raise ValueError("Distance too far back")

                while length > 0:
                    from_pos = (s.next - dist) % MAXWIN
                    b = s.window[from_pos]
                    s.window[s.next % MAXWIN] = b
                    s.output.append(b)
                    s.next += 1
                    length -= 1
                    if s.next >= MAXWIN:
                        s.first = False
            else:
                # Literal
                symbol = self.__litcode.decode(s) if lit else s.bits(8)
                s.window[s.next % MAXWIN] = symbol
                s.output.append(symbol)
                s.next += 1
                if s.next >= MAXWIN:
                    s.first = False

        return s.output

