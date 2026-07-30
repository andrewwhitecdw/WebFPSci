"""Regression test for readme parameter documentation consistency."""
import pathlib
import re

README = pathlib.Path(__file__).resolve().parent.parent / "readme.md"


def test_c2pvertpos_type_matches_default():
    content = README.read_text(encoding="utf-8")
    match = re.search(
        r"\*\s*(.+?):\s*`c2pVertPos`\s*\(`(\w+)`\)\s*=\s*`([^`]+)`",
        content,
    )
    assert match, "c2pVertPos entry not found in readme"
    label, ptype, default = match.groups()
    assert ptype == "Number", f"c2pVertPos should be Number, got {ptype}"
    assert label.strip().lower().startswith("vertical"), (
        f"c2pVertPos label should describe a vertical position, got {label!r}"
    )
    try:
        float(default)
    except ValueError:
        raise AssertionError(f"c2pVertPos default should be numeric, got {default!r}")


if __name__ == "__main__":
    test_c2pvertpos_type_matches_default()
    print("ok")
