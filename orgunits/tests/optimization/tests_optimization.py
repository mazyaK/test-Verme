"""
Copyright 2020 ООО «Верме»
"""

import pytest

from orgunits.models import Organization

pytestmark = [
    pytest.mark.django_db,
]


def test_get_tree_downwards_in_one_query(make_organization, django_assert_num_queries):
    parent = make_organization()
    make_organization(parent=parent)
    make_organization(parent=parent)
    make_organization(parent=parent)
    with django_assert_num_queries(1):
        list(Organization.objects.tree_downwards(parent.id))


def test_get_tree_upwards_in_one_query(make_organization, django_assert_num_queries):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_2)
    org_4 = make_organization(parent=org_3)
    with django_assert_num_queries(1):
        list(Organization.objects.tree_upwards(org_4.id))


def test_get_children_in_one_query(make_organization, django_assert_num_queries):
    parent = make_organization()
    make_organization(parent=parent)
    make_organization(parent=parent)
    make_organization(parent=parent)
    with django_assert_num_queries(1):
        list(parent.children())


def test_get_parents_in_one_query(make_organization, django_assert_num_queries):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_2)
    org_4 = make_organization(parent=org_3)
    with django_assert_num_queries(1):
        list(org_4.parents())
