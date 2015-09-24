import mwcli

router = mwcli.Router(
    "mwxml",
    "This script provides access to a set of utilities for extracting " +
        "content from MediaWiki XML dumps.",
    {'dump2revdocs': "Converts XML dumps to revision documents (XML --> JSON)"}
)

main = router.main
