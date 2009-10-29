# This file is necessary to make this directory a package.

try:
    # Declare this a namespace package if pkg_resources is available.
    import pkg_resources
    pkg_resources.declare_namespace('getpaid')
except ImportError:
    pass

