"""Regression test for CSS length units."""
import pathlib
import re
import sys

CSS = pathlib.Path("css/main.css").read_text()

def test_font_size_has_unit():
    for decl in re.findall(r"font-size\s*:\s*([^;]+);", CSS):
        val = decl.strip()
        if val == "0":
            continue
        if not re.search(r"\d+(px|pt|em|rem|%|vh|vw|vmin|vmax|ex|ch|cm|mm|in|pc)$", val):
            raise AssertionError(f"font-size value {val!r} is missing a unit")

if __name__ == "__main__":
    test_font_size_has_unit()
    print("OK")
