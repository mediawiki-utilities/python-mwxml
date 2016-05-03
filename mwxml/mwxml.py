import mwcli

router = mwcli.Router(
    "mwxml",
    "This script provides access to a set of utilities for extracting " +
        "content from MediaWiki XML dumps.",
    {'dump2revdocs': "Converts XML dumps to revision documents (XML --> JSON)",
     'validate': "Compares a stream of revision documents against a schema",
     'normalize': "Converts a stream of old revision documents to documents " +
                  "that validate against the current schema",
     'inflate': "Converts a stream of flat revision documents to standard " +
                "revision documents"}
)

main = router.main
