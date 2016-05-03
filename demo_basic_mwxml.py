"""
Count revisions saved by anonymous editors
"""
import sys

import mwxml


def process_dump(dump, path):
    for page in dump:
        yield sum(revision.user.id is None
                  for revision in page)

dump_paths = sys.argv[1:]
print(sum(mwxml.map(process_dump, dump_paths)))
