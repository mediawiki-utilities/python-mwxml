"""
Validates a stream of JSON revsion documents against a JSON schema and writes
them to stdout if they validate -- otherwise, complains noisily.

Usage:
    validate (-h|--help)
    validate [<input-file>...] --schema=<path> [--threads=<num>]
             [--output=<path>] [--compress=<type>] [--verbose] [--debug]

Options:
    -h|--help           Print this documentation
    <input-file>        The path to file containing a sequence of JSON
                        revision documents [default: <stdin>]
    --schema=<path>     The path to a schema to apply.
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
import json

import jsonschema
import mwcli


def process_args(args):
    return {'schema': json.load(open(args['--schema']))}


def validate(docs, schema, verbose=False):
    for doc in docs:
        jsonschema.validate(doc, schema)
        yield doc

streamer = mwcli.Streamer(
    __doc__,
    __name__,
    validate,
    process_args
)

main = streamer.main
