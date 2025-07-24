"""
dbc-to-dbf

A Python library for converting .dbc (compressed DBF) files into standard .dbf format,
using a reimplementation of the BLAST decompression algorithm by Mark Adler.

Author: Mozar Silva
License: zlib
"""

from .blast_decompress import BlastDecompress
from .dbc_decompress import DBCDecompress

__all__ = ["BlastDecompress", "DBCDecompress"]
__version__ = "1.0.0"
