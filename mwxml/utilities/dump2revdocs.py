r"""
``$ mwxml dump2revdocs -h``
::

    Converts MediaWiki XML dumps to page-partitioned sequences of revision JSON
    documents.

    Usage:
        dump2revdocs (-h|--help)
        dump2revdocs [<input-file>...] [--threads=<num>] [--output=<path>]
                     [--compress=<type>] [--verbose] [--debug]

    Options:
        -h|--help           Print this documentation
        <input-file>        The path to a MediaWiki XML Dump file
                            [default: <stdin>]
        --threads=<num>     If a collection of files are provided, how many
                            processor threads? [default: <cpu_count>]
        --output=<path>     Write output to a directory with one output file
                            per input path.  [default: <stdout>]
        --compress=<type>   If set, output written to the output-dir will be
                            compressed in this format. [default: bz2]
        --verbose           Print progress information to stderr.  Kind of a
                            mess when running multi-threaded.
        --debug             Print debug logs.
"""
import sys

import mwcli

from ..iteration import Dump


def dump2revdocs(dump, verbose=False):
    for page in dump:

        if verbose:
            sys.stderr.write(page.title + ": ")
            sys.stderr.flush()

        for revision in page:
            yield revision.to_json()

            if verbose:
                sys.stderr.write(".")
                sys.stderr.flush()

        if verbose:
            sys.stderr.write("\n")
            sys.stderr.flush()


def process_args(args):
    return {}

streamer = mwcli.Streamer(
    __doc__,
    __name__,
    dump2revdocs,
    process_args,
    file_reader=Dump.from_file
)

main = streamer.main
