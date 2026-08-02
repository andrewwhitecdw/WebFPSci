"""Regression test for open_localhost.bat race condition."""
import pathlib
import re

BAT = pathlib.Path(__file__).resolve().parent.parent / "open_localhost.bat"


def test_server_start_before_browser():
    content = BAT.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("::")]
    server_idx = next((i for i, line in enumerate(lines) if "http.server" in line), None)
    browser_idx = next((i for i, line in enumerate(lines) if "localhost:8000/index.html" in line), None)
    assert server_idx is not None, "missing server start command"
    assert browser_idx is not None, "missing browser open command"
    assert browser_idx > server_idx, "browser command must come after server start"
    middle = lines[server_idx + 1:browser_idx]
    readiness_pattern = re.compile(
        r"s\.connect|socket\.connect|Test-NetConnection|TcpClient|"
        r"127\.0\.0\.1\s*[:',]\s*8000|localhost\s*[:',]\s*8000",
        re.IGNORECASE,
    )
    assert any(readiness_pattern.search(line) for line in middle), (
        "expected a readiness probe that verifies the server is accepting connections"
    )


if __name__ == "__main__":
    test_server_start_before_browser()
    print("ok")
