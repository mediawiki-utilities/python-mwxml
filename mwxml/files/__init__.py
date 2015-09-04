"""
This module contains a set of functions for checking and opening compressed
files.  Currently, there are 4 compression formats supported:

:Compression formats:
    plain text : `*.xml`
        A plaintext XML file.
    gzip : `*.gz`
        A gzip compressed file.
    bzip2 : `*.bz2`
        A bzip2 compressed file.
    7-Zip : `*.7z`
        An LZMA-based archiver format.  Note that processing files with this
        compression format requires that the p7zip utility is installed on
        system.  See http://packages.ubuntu.com/search?keywords=p7zip-full

Functions
---------
.. automodule:: mwxml.files.functions
"""
from .functions import open, normalize_path, concat, extract_extension

__all__ = [open, normalize_path, concat, extract_extension]
