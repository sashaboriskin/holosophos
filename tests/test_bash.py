import os

from holosophos.tools.bash import bash, WORKSPACE_DIR

def test_bash():
    result = bash('echo "Hello World"')
    assert result == "Hello World"

    result = bash("pwd")
    assert result == "/workspace"

    result = bash("touch dummy")
    assert os.path.exists(WORKSPACE_DIR / "dummy")

    result = bash("fddafad")
    assert "fddafad: command not found" in result
