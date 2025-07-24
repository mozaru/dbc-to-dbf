"""
BLAST decompressor - Python version
Originally based on blast.c by Mark Adler (zlib license)
Ported and extended by Mozar Silva - 2025

Licensed under the zlib License (see LICENSE file for details).
"""

import sys
from blastDecompress import BlastDecompress

class DBCDecompress (BlastDecompress):
    
    def decompress(self, raw_data:bytes) -> bytes:
        #get header size in bytes Little-endian (LSB-first)
        header_size = raw_data[8] + (raw_data[9] << 8)

        #same header input to output, but last byte is 0x0D
        header_data = raw_data[:header_size-1]+bytes([0x0D])

        #after header size + 4, compress data with blaze 
        compressed_data = raw_data[header_size+4:]
        return header_data+super().decompress(compressed_data)

    def decompressFile(self, input_path:str, output_path:str):
        with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
            # infile.seek(8)
            # raw_header = infile.read(2)
            # header = raw_header[0] + (raw_header[1] << 8)

            # infile.seek(0)
            # header_data = infile.read(header)
            # header_data = bytearray(header_data)
            # header_data[header - 1] = 0x0D
            # outfile.write(header_data)

            # infile.seek(header + 4)
            # compressed_data = bytearray(infile.read())

            # # Aqui entraria a parte de descompressão equivalente ao `blast()`
            # decompressed = self.decompress(compressed_data)
            # outfile.write(decompressed)
            outfile.write(self.decompress(infile.read()))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python dbc2dbf.py <arquivo_entrada.dbc> <arquivo_saida.dbf>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        dbc2dbf = DBCDecompress()
        dbc2dbf.decompressFile(input_file, output_file)
        print(f"Conversão concluída: {output_file}")
    except Exception as e:
        print(f"Erro ao converter arquivo: {e}")
        sys.exit(1)