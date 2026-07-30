import re
from pathlib import Path

BAT = Path(__file__).resolve().parent.parent / 'open_localhost.bat'


def test_script_switches_to_its_own_directory():
    text = BAT.read_text()
    assert 'cd /d "%~dp0"' in text, (
        "Script should cd to its own directory before serving"
    )


def test_script_waits_for_server_before_opening_browser():
    text = BAT.read_text()
    server_idx = text.index('start py -m http.server 8000')
    browser_idx = text.index('start http://localhost:8000/index.html')
    between = text[server_idx:browser_idx]
    assert re.search(r'\b(timeout|ping)\b', between, re.IGNORECASE), (
        "Expected a wait/sleep between starting server and opening browser"
