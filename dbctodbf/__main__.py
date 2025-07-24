import sys
from .dbc_decompress import DBCDecompress

def main():
    if len(sys.argv) != 3:
        print("Uso: python -m dbctodbf <entrada.dbc> <saida.dbf>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        dbc2dbf = DBCDecompress()
        dbc2dbf.decompressFile(input_file, output_file)
        print(f"Conversão concluída: {output_file}")
    except Exception as e:
        print(f"Erro ao converter: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
