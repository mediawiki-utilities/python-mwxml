r"""
``$ mwxml normalize -h``
::

    Converts a stream of RevisionDocument JSON blobs that validated against any
    past schemas into JSON blobs that will validate against the latest schema.

    Usage:
        normalize (-h|--help)
        normalize [<input-file>...] [--threads=<num>] [--output=<path>]
                  [--compress=<type>] [--verbose] [--debug]

    Options:
        -h|--help           Print this documentation
        <input-file>        The path to file containing a sequence of JSON
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


def normalize(rev_docs, verbose=False):

    for rev_doc in rev_docs:
        changed = False
        if 'page' in rev_doc:
            # Converts page.redirect_title to page.redirect
            if 'redirect_title' in rev_doc['page']:
                rev_doc['page']['redirect'] = rev_doc['page']['redirect_title']
                del rev_doc['page']['redirect_title']
                changed = True

            # Converts page.redirect.title to page.redirect
            if 'redirect' in rev_doc['page'] and \
               isinstance(rev_doc['page']['redirect'], dict) and \
               'title' in rev_doc['page']['redirect']:

                rev_doc['page']['redirect'] = \
                    rev_doc['page']['redirect']['title']

                # No deletion necessary since we're replacing the old key
                changed = True

        if 'contributor' in rev_doc:
            contributor_doc = rev_doc['contributor'] or {}
            user_doc = {}
            if 'id' in contributor_doc:
                user_doc['id'] = contributor_doc['id']
            if 'user_text' in contributor_doc:
                user_doc['text'] = contributor_doc['user_text']

            rev_doc['user'] = user_doc
            del rev_doc['contributor']
            changed = True

        changed = trim_dict(rev_doc) or changed

        if verbose:
            if changed:
                sys.stderr.write("!")
            else:
                sys.stderr.write(".")
            sys.stderr.flush()

        yield rev_doc


def trim_dict(d):
    changed = False
    keys_to_del = []
    for key, value in d.items():
        if value is None:
            keys_to_del.append(key)
        elif isinstance(value, dict):
            changed = trim_dict(value)
            if len(value) == 0:
                keys_to_del.append(key)
    if len(keys_to_del) > 0:
        changed = True
    for key in keys_to_del:
        del d[key]
    return changed

streamer = mwcli.Streamer(
    __doc__,
    __name__,
    normalize
)
main = streamer.main
