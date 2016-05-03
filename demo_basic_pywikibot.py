"""
Count revisions saved by anonymous editors
"""
import sys

import pywikibot.xmlreader

ip_edits = 0
dump_paths = sys.argv[1:]

for path in dump_paths:
    dump = pywikibot.xmlreader.XmlDump(path, allrevisions=True)
    for entry in dump.parse():
        ip_edits += entry.ipedit

print(ip_edits)
