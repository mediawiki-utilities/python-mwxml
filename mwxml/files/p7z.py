import os
import subprocess

file_open = open


def open(path):
    """
    Turns a path to a dump file into a file-like object of (decompressed)
    XML data assuming that '7z' is installed and will know what to do.

    :Parameters:
        path : `str`
            the path to the dump file to read
    """
    p = subprocess.Popen(
        ['7z', 'e', '-so', path],
        stdout=subprocess.PIPE,
        stderr=file_open(os.devnull, "w")
    )
    return p.stdout
