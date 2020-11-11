"""
Copyright 2020 ООО «Верме»
"""

import pytest

from wfm.test import mixer as _mixer
from wfm.test.api_client import DRFClient


@pytest.fixture()
def api(db, settings):
    settings.AXES_ENABLED = False
    return DRFClient()


@pytest.fixture()
def anon(db):
    return DRFClient(anon=True)


@pytest.fixture()
def mixer():
    return _mixer
