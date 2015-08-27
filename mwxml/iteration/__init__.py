"""
These classes form the basis of iterative processing of XML dumps.  These
datatypes are based on those found in http://pythonhosted.org/mwtypes

.. autoclass:: mwxml.iteration.dump.Dump
    :members:

.. autoclass:: mwxml.iteration.site_info.SiteInfo

.. autoclass:: mwxml.iteration.page.Page
    :inherited-members:

.. autoclass:: mwxml.iteration.revision.Revision
    :inherited-members:

.. autoclass:: mwxml.iteration.namespace.Namespace
    :inherited-members:

"""
from .dump import Dump
from .page import Page
from .revision import Revision
from .site_info import SiteInfo
