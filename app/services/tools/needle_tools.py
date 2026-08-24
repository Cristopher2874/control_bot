import needle
import logging
from io import BytesIO
from pathlib import Path

from app.utils.prompts import ESSAY_TOOL_PROMPT

logger = logging.getLogger(__name__)


def _markdown_to_pdf_bytes(md_content: str) -> bytes:
    """Render Markdown to validated PDF bytes without touching the target file."""
    import markdown
    from xhtml2pdf import pisa

    html_body = markdown.markdown(md_content)
    html_content = f"""
    <html>
    <head>
    <style>
        @page {{
            size: letter;
            margin: 1in;
        }}
        body {{
            font-family: Helvetica, Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.5;
            text-align: justify;
        }}
        h1 {{ text-align: center; font-size: 24pt; margin-bottom: 0.5in; }}
        h2 {{ font-size: 18pt; margin-top: 0.3in; }}
        h3 {{ font-size: 14pt; }}
        p {{ margin-bottom: 0.1in; }}
    </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    output = BytesIO()
    status = pisa.CreatePDF(html_content, dest=output)
    pdf_bytes = output.getvalue()

    if status.err:
        raise RuntimeError(f"xhtml2pdf reported {status.err} conversion error(s)")
    if not pdf_bytes.startswith(b"%PDF-"):
        raise RuntimeError("PDF converter returned data without a PDF header")

    return pdf_bytes

@needle.tool
def get_weather(city: str):
    "Get the current weather for a city."
    return {"city": city, "temp_c": 27, "sky": "clear"}

@needle.tool
def write_essay(topic: str, length: str):
    """Write an essay based on a given topic and provided length for it, returns the final essay"""
    from app.services.llm_service import get_llm_service

    prompt = ESSAY_TOOL_PROMPT + f"\nTopic: {topic}" + f"\nLength: {length}"

    logger.info("Calling essay LLM")
    response = get_llm_service().call_agent(prompt=prompt)
    logger.info("Response generated from essay LLM")

    md_content = response
    if not md_content.strip():
        raise RuntimeError("Essay LLM returned empty content")

    # Define paths
    md_relative_path = f"llm_gens/{topic}.md"
    pdf_relative_path = f"llm_gens/{topic}.pdf"

    repo_root = Path.cwd().resolve()
    md_target_file = repo_root / md_relative_path
    pdf_target_file = repo_root / pdf_relative_path

    # Ensure directory exists
    md_target_file.parent.mkdir(parents=True, exist_ok=True)

    # 1. Save the Markdown file
    md_target_file.write_text(md_content, encoding='utf-8')

    try:
        pdf_bytes = _markdown_to_pdf_bytes(md_content)
        temporary_pdf_file = pdf_target_file.with_suffix(".pdf.tmp")
        temporary_pdf_file.write_bytes(pdf_bytes)
        temporary_pdf_file.replace(pdf_target_file)

    except Exception as e:
        logger.exception("PDF generation failed for topic %r: %s", topic, e)
        return {"response": f"Generated MD file to {md_target_file}, but encountered an error creating the PDF."}

    logger.info(f"Generated files to {md_target_file} and {pdf_target_file}")
    return {"response": f"Generated files to {md_target_file} and {pdf_target_file}"}

TOOLS = [get_weather, write_essay]