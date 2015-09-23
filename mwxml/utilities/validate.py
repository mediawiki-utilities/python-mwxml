"""
Validates a stream of JSON revsion documents against a JSON schema and writes
them to stdout if they validate -- otherwise, complains noisily.

Usage:
    validate (-h|--help)
    validate <schema>

Options:
    -h|--help      Print this documentation
    <schema>       The path of a JSON schema to use for validation
"""
import json
import sys

import docopt
import jsonschema


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    schema = json.load(open(args['<schema>']))

    run((json.loads(line) for line in sys.stdin), schema)

def run(docs, schema):

    for doc in jsonvalidate(docs, schema):
        json.dump(doc, sys.stdout)
        sys.stdout.write("\n")

def jsonvalidate(docs, schema):
    for doc in docs:
        jsonschema.validate(doc, schema)
        yield doc
