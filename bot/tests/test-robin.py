
from ..modules.robin import Robin
import pytest


def test_sanitize():
    robin = Robin()
    assert robin._sanitize(msg_in='Dit is een teststring') == 'Dit is een teststring'
    assert robin._sanitize(msg_in='TestString met een at @') == 'TestString met een at _'
    assert robin._sanitize(msg_in='TestString met een hash #') == 'TestString met een hash _'