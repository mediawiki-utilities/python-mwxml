"""
Count revisions saved by anonymous editors
"""
import sys

import mwxml


def process_dump(dump, path):
    for page in dump:
        for revision in page:
            if revision.user.id is None:
                yield 1

dump_paths = sys.argv[1:]
print(sum(mwxml.map(process_dump, dump_paths)))
