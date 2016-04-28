r"""
``$ mwxml inflate -h``
::

    Converts a stream of flat RevisionDocument JSON blobs into hierarchical JSON
    RevisionDocument JSON blobs.

    Usage:
        inflate (-h|--help)
        inflate [<input-file>...] [--threads=<num>] [--output=<path>]
                [--compress=<type>] [--verbose] [--debug]

    Options:
        -h|--help           Print this documentation
        <input-file>        The path to file containing a sequence of flat JSON
                            revision documents [default: <stdin>]
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


def _single_inflate(flat_json):
    inflated = {}
    flat_keys = flat_json.keys()
    for key in flat_keys:
        bottom_dict = inflated
        parts = key.split('_')
        for sub_key in parts[:-1]:
            if sub_key not in bottom_dict:
                bottom_dict[sub_key] = {}
            bottom_dict = bottom_dict[sub_key]
        bottom_dict[parts[-1]] = flat_json[key]
    return inflated


def inflate(flat_jsons, verbose=False):
    for flat_json in flat_jsons:
        inflated = _single_inflate(flat_json)
        yield inflated


streamer = mwcli.Streamer(
    __doc__,
    __name__,
    inflate
)
main = streamer.main
