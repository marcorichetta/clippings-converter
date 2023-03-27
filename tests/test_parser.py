from datetime import datetime
import pytest

from converter import Clipping, generate_markdown

@pytest.mark.skip(reason="No se como declarar que un classmethod devuelve una lista de instancias de la misma clase")
def test_parse_file_returns_list_of_clippings():

    clippings = Clipping.parse_file(clippings_file="tests/clippings_full.txt")

    assert isinstance(clippings, list(Clipping))

def test_parse_single_clipping():

    clippings: list[Clipping] = Clipping.parse_file(clippings_file="tests/single_clipping.txt")

    assert clippings[0].title == "Benjamin Franklin: An American Life"
    assert clippings[0].author == "Walter Isaacson"
    assert clippings[0].page == 337
    assert clippings[0].date == datetime(2016, 8, 6, 2, 25, 21)
    assert clippings[0].note == "In what became known as “Hume’s fork,” the great Scottish philosopher, along with Leibniz and others, had developed a theory that distinguished between synthetic truths that describe matters of fact (such as “London is bigger than Philadelphia”) and analytic truths that are self-evident by virtue of reason and definition (“The angles of a triangle equal 180 degrees”; “All bachelors are unmarried”)."

def test_parse_file_without_page_sets_it_to_0():

    clippings = Clipping.parse_file(clippings_file="tests/clipping_without_page.txt")

    assert clippings[0].page == 0