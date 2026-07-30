"""Regression test for body-contained markup."""
import pathlib
import sys

HTML = pathlib.Path("index.html").read_text()
BODY_END = HTML.lower().find("</body>")

def test_media_and_inputs_inside_body():
    for tag in ("<audio", "<input"):
        idx = HTML.lower().find(tag)
        if idx == -1:
            continue
        assert idx < BODY_END, (
            f"{tag} tag found after </body>; interactive elements must be inside <body>"
        )

if __name__ == "__main__":
    test_media_and_inputs_inside_body()
    print("OK")
