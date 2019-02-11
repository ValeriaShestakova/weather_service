import pytest

from Tests_task.person import Person


@pytest.fixture()
def person_without_address():
    return Person('Alexander', 1799, '')


@pytest.fixture()
def person():
    return Person('Alexander', 1799, 'Moscow')


def test_default_initial_address(person_without_address):
    assert person_without_address.address == ''


def test_setting_initial_attributes(person):
    assert person.name == 'Alexander'
    assert person.address == 'Moscow'
    assert person.yob == 1799


def test_person_get_age(person):
    assert person.get_age() == 220


def test_person_get_name(person):
    assert person.get_name() == "Alexander"


def test_person_set_name(person):
    person.set_name('Sasha')
    assert person.name == 'Sasha'


def test_set_address(person):
    person.set_address('Spb')
    assert person.address == 'Spb'


@pytest.mark.parametrize("address, expected", [
    ('Moscow', False),
    ('', True),
    (None, True),
])
def test_is_homeless(person, address, expected):
    person.set_address(address)
    assert person.is_homeless() is expected
