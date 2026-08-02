"""Regression test for open_localhost.bat race condition."""
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

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


def test_readiness_probe_waits_for_server():
    if sys.platform != "win32":
        # The .bat script is Windows-specific.
        return
    with tempfile.TemporaryDirectory() as tmp:
        pathlib.Path(tmp, "index.html").write_text("<html>hello</html>", encoding="utf-8")
        server = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000"],
            cwd=tmp,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            content = BAT.read_text(encoding="utf-8")
            probe_line = None
            for line in content.splitlines():
                if line.strip().startswith("py -c"):
                    probe_line = line.strip()
                    break
            assert probe_line is not None, "missing readiness probe"
            probe_code = probe_line[len("py -c"):].strip().strip('"')
            result = subprocess.run(
                [sys.executable, "-c", probe_code],
                timeout=35,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"readiness probe failed: {result.stderr}"
            with urllib.request.urlopen("http://localhost:8000/index.html", timeout=5) as resp:
                assert resp.status == 200
                assert "hello" in resp.read().decode("utf-8")
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    test_server_start_before_browser()
    test_readiness_probe_waits_for_server()
    print("ok")
