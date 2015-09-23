r"""
``$ mwxml dump2revdocs -h``
::

    Converts MediaWiki XML dumps to page-partitioned sequences of revision JSON
    documents.

    Usage:
        dump2revdocs (-h|--help)
        dump2revdocs [<dump-file>...] [--threads=<num>] [--output=<path>]
                     [--compress=<type>] [--verbose]

    Options:
        -h|--help           Print this documentation
        <dump-file>         The path to a MediaWiki XML Dump file
                            [default: <stdin>]
        --threads=<num>     If a collection of files are provided, how many
                            processor threads? [default: <cpu_count>]
        --output=<path>     Write output to a directory with one output file
                            per input path.  [default: <stdout>]
        --compress=<type>   If set, output written to the output-dir will be
                            compressed in this format. [default: bz2]
        --verbose           Print progress information to stderr.  Kind of a
                            mess when running multi-threaded.
"""
import json
import logging
import sys
import time
from multiprocessing import cpu_count

import docopt
import mwtypes.files
import yamlconf

from ..map import map

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    if len(args['<dump-file>']) == 0:
        paths = [sys.stdin]
    else:
        paths = args['<dump-file>']

    if args['--threads'] == "<cpu_count>":
        threads = cpu_count()
    else:
        threads = int(args['--threads'])

    if args['--output'] == "<stdout>":
        output_dir = None
        logger.info("Writing output to stdout.  Ignoring 'compress' setting.")
        compression = None
    else:
        output_dir = files.normalize_dir(args['--output'])
        compression = args['--compress']

    verbose = bool(args['--verbose'])

    run(paths, threads, output_dir, compression, verbose)


def run(paths, threads, output_dir, compression, verbose):

    def process(dump, path):
        rev_docs = dump2revdocs(dump, verbose=verbose)

        if output_dir == None:
            yield from rev_docs
        else:
            new_path = files.output_dir_path(path, output_dir, compression)
            writer = files.writer(new_path)
            for rev_doc in rev_docs:
                json.dump(rev_doc, writer)
                writer.write("\n")

    for rev_doc in map(process, paths, threads=threads):
        json.dump(rev_doc, sys.stdout)
        sys.stdout.write("\n")

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
