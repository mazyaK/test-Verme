"""
Copyright 2020 ООО «Верме»
"""

import pytest

from orgunits.models import Organization

pytestmark = [
    pytest.mark.django_db,
]


def test_str(organization):
    assert str(organization) == organization.name


def test_get_tree_downwards_no_children(make_organization):
    org_1 = make_organization()
    org_2 = make_organization()
    assert org_2 not in Organization.objects.tree_downwards(org_1.id)
    assert org_1 not in Organization.objects.tree_downwards(org_2.id)


def test_get_tree_downwards_cluster(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_1)
    children = Organization.objects.tree_downwards(org_1.id)
    assert org_1 in children
    assert org_2 in children
    assert org_3 in children


def test_get_tree_downwards_chain(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_2)
    children = Organization.objects.tree_downwards(org_1.id)
    assert org_1 in children
    assert org_2 in children
    assert org_3 in children


def test_get_tree_downwards_half_chain(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_2)
    children = Organization.objects.tree_downwards(org_2.id)
    assert org_1 not in children
    assert org_2 in children
    assert org_3 in children


def test_get_parents_chain(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_2)
    parents = Organization.objects.tree_upwards(org_3.id)
    assert org_1 in parents
    assert org_2 in parents
    assert org_3 in parents


def test_get_parents_half_chain(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    org_3 = make_organization(parent=org_2)
    parents = Organization.objects.tree_upwards(org_2.id)
    assert org_1 in parents
    assert org_2 in parents
    assert org_3 not in parents


def test_get_children(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    assert org_1 not in org_1.children()
    assert org_2 in org_1.children()
    assert not org_2.children().exists()


def test_get_parents(make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    assert org_2 not in org_2.parents()
    assert org_1 in org_2.parents()
    assert not org_1.parents().exists()
