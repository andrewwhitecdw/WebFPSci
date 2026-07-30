from pathlib import Path

README = Path(__file__).resolve().parent.parent / 'readme.md'


def test_title_spells_javascript_correctly():
    first_line = README.read_text().splitlines()[0]
    assert 'Javscript' not in first_line
