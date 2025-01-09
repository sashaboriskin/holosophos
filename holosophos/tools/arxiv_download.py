import pathlib

import requests
from marker.converters.pdf import PdfConverter  # type: ignore
from marker.models import create_model_dict  # type: ignore
from marker.output import text_from_rendered  # type: ignore

DIR_PATH = pathlib.Path(__file__).parent
ROOT_PATH = DIR_PATH.parent.parent
WORKSPACE_DIR = ROOT_PATH / "workdir"


def arxiv_download(paper_id: str) -> str:
    """
    A tool that downloads papers from Arxiv and converts them to text.

    Args:
        paper_id: ID of the paper on Arxiv. For instance: 2409.06820v1
    """

    pdf_output_filename = WORKSPACE_DIR / f"{paper_id}.pdf"
    if not pdf_output_filename.exists():
        pdf_url = f"https://arxiv.org/pdf/{paper_id}"
        response = requests.get(pdf_url)
        content_type = response.headers.get("content-type")
        assert content_type
        assert "application/pdf" in content_type.lower()
        with open(pdf_output_filename.resolve(), "wb") as fp:
            fp.write(response.content)
    md_output_filename = WORKSPACE_DIR / f"{paper_id}.md"
    text = ""
    if not md_output_filename.exists():
        converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )
        rendered = converter(str(pdf_output_filename.resolve()))
        text, _, images = text_from_rendered(rendered)
        with open(md_output_filename.resolve(), "w") as fp:
            fp.write(text)
    else:
        with open(md_output_filename.resolve()) as r:
            text = r.read()
    return text
