import json
from pathlib import Path

import pytest

from fairdm.contrib.contributors import utils

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def ror_data():
    with open(DATA_DIR / "ror.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def orcid_data():
    with open(DATA_DIR / "orcid.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.mark.django_db
def test_contributor_from_ror_data_object(ror_data):
    org = utils.contributor_from_ror_data(ror_data)
    assert org.pk is not None
    assert org.name == "PSL Research University"
    assert org.city == "Paris"
    assert org.country == "France"
    assert org.ror == ror_data
    assert len(org.links) == 2  # data["links"] + data["wikipedia_url"]
    assert len(org.alternative_names) == 2  # data["aliases"] + data["acronyms"]
    assert "Université PSL" in org.alternative_names
    assert "PSL" in org.alternative_names
    assert org.identifiers.count() == 5  # 4 from data["external_ids"] + 1 from data["id"]


@pytest.mark.django_db
def test_contributor_from_orcid_data_object(orcid_data):
    person = utils.contributor_from_orcid_data(orcid_data)
    assert person.pk is not None
    assert person.name == "Samuel Jennings"
    assert person.profile == "A test biography"
    assert len(person.links) == 0  # data["links"] + data["wikipedia_url"]
    assert len(person.alternative_names) == 1  # data["aliases"] + data["acronyms"]
    assert "Sam Jennings" in person.alternative_names
    # assert org.identifiers.count() == 5  # 4 from data["external_ids"] + 1 from data["id"]

    assert person.identifiers.filter(type="ORCID", value="0000-0003-3762-7336").exists()
