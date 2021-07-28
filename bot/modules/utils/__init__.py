"""
All related to whitestar functionality
"""
import locale
import os
from .feedback import *
from .sanitize import *
from .normalize_time import *
from .rolemembers import *
from .get_all_roles import *
from .in_role import *
from .ping import *

# try:
#     locale.setlocale(locale.LC_ALL, "nl_NL.utf8")  # required running on linux
#     logger.info("running on linux")
# except locale.Error:
#     locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")  # required when running on MAC
#     logger.info("running on mac")
