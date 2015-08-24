class FileTypeError(Exception):
    """
    Thrown when an XML dump file is not of an expected type.
    """
    pass


class MalformedXML(Exception):
    """
    Thrown when an XML dump file is not formatted as expected.
    """
    pass
