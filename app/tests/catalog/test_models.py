# tests/catalog/test_models.py
from catalog.models import Group, Category


def test_group(db, django_db_setup):
    """
        # Given a database pre-populated with groups,
        # verify groups.
    """
    groups = Group.objects.all()
    assert len(groups) == 4

    gp1 = Group.objects.get(id=1)
    gp2 = Group.objects.get(id=2)
    gp3 = Group.objects.get(id=3)
    gp4 = Group.objects.get(id=4)
    assert gp1.name == 'Group 1'
    assert gp1.description == 'Test group 1'
    assert gp2.name == 'Group 2'
    assert gp2.description == 'Test group 2'
    assert gp3.name == 'Group 3'
    assert gp3.description == 'Test group 3'
    assert gp4.name == 'Group 4'
    assert gp4.description == 'Test group 4'


def test_category(db, django_db_setup):
    """
            # Given a database pre-populated with fixtures,
            # verify category is correct.
    """
    cats = Category.objects.all()
    assert len(cats) == 4