from holosophos.tools import arxiv_download


def test_arxiv_download() -> None:
    result = arxiv_download("2409.06820")
    assert "pingpong" in result.lower()
