# dbc-to-dbf

A pure Python utility to convert `.dbc` files into standard `.dbf` format — commonly used in public health data from the Brazilian government.

`.dbc` files are a compressed form of `.dbf` (dBase format) files used by **DATASUS**, the Department of Informatics of the **Brazilian Unified Health System (SUS)**.  
DATASUS provides large-scale public health datasets (such as hospital admissions, mortality records, disease surveillance, and more) in `.dbc` format to reduce file size and facilitate distribution.

These `.dbc` files are compressed using a legacy algorithm known as **PKWare DCL "implode"**, originally used in older versions of ZIP files. This format is no longer widely supported, and modern decompression libraries (like `zipfile` or `gzip`) **do not handle `.dbc` files**.

This project provides a **pure Python implementation** of the **BLAST decompression algorithm**, which is compatible with the compression used in `.dbc` files. It is a direct, object-oriented rewrite of `blast.c` by Mark Adler (co-author of zlib), adapted and modernized for Python usage.

With this library, researchers, data analysts, public health professionals, and developers can easily **extract health data from DATASUS** in a readable and processable format — enabling analysis, dashboards, research, and more.

---

## References

- DATASUS homepage: [https://datasus.saude.gov.br](https://datasus.saude.gov.br)
- File format documentation (Portuguese): [https://ftp.datasus.gov.br/](https://ftp.datasus.gov.br/)
- Compression format background: [https://github.com/madler/blast](https://github.com/madler/blast)

---

## 📦 Installation

Install directly from PyPI:

    pip install dbc-to-dbf

Or clone from GitHub and install locally:

    git clone https://github.com/mozaru/dbc-to-dbf.git
    cd dbc-to-dbf
    pip install .

---

## 🚀 Usage


### ➤ Option 1: Import and use in Python code

```python
from dbctodbf import DBCDecompress

dbc = DBCDecompress()
dbc.decompressFile("input.dbc", "output.dbf")
```

### ➤ Option 2: Run as a module

```bash
python -m dbctodbf input.dbc output.dbf
```

### ➤ Option 3: Use CLI command (installed with pip)

```bash
dbc2dbf input.dbc output.dbf
```

---

## 🔧 Features

- Fully implemented in pure Python (no native extensions)
- Converts `.dbc` (compressed DBF) to `.dbf`
- Based on Mark Adler's `blast.c`, adapted and improved using modern Python
- Object-oriented design for easy integration and reuse
- Easily testable and extendable

---

## 🖥️ Example CLI script (for custom use)

```python

    import sys
    from dbctodbf import DBCDecompress

    if __name__ == "__main__":
        if len(sys.argv) != 3:
            print("Uso: python script.py <entrada.dbc> <saida.dbf>")
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
```

---

## 🔗 Links

- 📂 GitHub: [https://github.com/mozaru/dbc-to-dbf](https://github.com/mozaru/dbc-to-dbf)
- 📦 PyPI: _(coming soon)_

---

## 🧑‍💻 Contributing

Pull requests are welcome!  
If you find a bug or have a suggestion, feel free to open an issue.

---

## ⚖️ License

This project is licensed under the zlib License (see LICENSE file).

Original decompression algorithm by Mark Adler <madler@alumni.caltech.edu>  
Python port and enhancements by Mozar Silva <mozar.silva@11tech.com.br> or <mozar.silva@gmail.com.br>.

