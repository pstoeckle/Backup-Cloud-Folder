# -*- coding: utf-8 -*-
"""
Main module.
"""
from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "backup-cloud-folder"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
__author__ = "Patrick Stöckle"
__copyright__ = "Patrick Stöckle"
__license__ = "apache-2.0"
