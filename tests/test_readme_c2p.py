import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / 'readme.md'


def test_c2pvertpos_documented_as_number():
    text = README.read_text()
    match = re.search(
        r'Vertical position: `c2pVertPos` \((`[^`]+`)\) = `0\.5`', text
    )
    assert match, "c2pVertPos line not found or malformed"
    assert match.group(1) == '`Number`', (
        f"Expected Number type, got {match.group(1)}"
    )
