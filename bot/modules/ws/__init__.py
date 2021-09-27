"""
All related to whitestar functionality
"""
import locale
import os
import datetime
from datetime import timedelta, datetime
from .comeback import *
from .status import *
from .entry import *

try:
    locale.setlocale(locale.LC_ALL, "nl_NL.utf8")  # required running on linux
    logger.info("running on linux")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")  # required when running on MAC
    logger.info("running on mac")
