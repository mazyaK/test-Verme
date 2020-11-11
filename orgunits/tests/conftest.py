"""
Copyright 2020 ООО «Верме»
"""

import pytest

from orgunits.models import Organization

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def organization(mixer):
    return mixer.blend(Organization)


@pytest.fixture()
def make_organization(mixer):
    def _organization_generator(**kwargs):
        return mixer.blend(Organization, **kwargs)
    return _organization_generator
