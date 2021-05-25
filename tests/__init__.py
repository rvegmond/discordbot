"""
the content of this file should cover the generic functionality..
"""
import os
import sys
from mock import patch
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


def mock_decorator(name=None, help=None, brief=None, hidden=None):
    """
    Might not be the best cleanest way to mock the commands.command
    decorator, but this seems to work, maybe in the future a better solution
    will come along..
    """
    def decorator(f):
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


mockje = patch('discord.ext.commands.command', mock_decorator).start()
