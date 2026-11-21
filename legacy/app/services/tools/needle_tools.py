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
def draft_or_edit_essay(topic: str, length: str = "", feedback: str = ""):
    """
    Draft a new essay or edit an existing one based on user feedback. 
    Returns the markdown content for the user to review.
    """
    from app.services.llm_service import get_llm_service

    repo_root = Path.cwd().resolve()
    md_relative_path = f"llm_gens/{topic}.md"
    md_target_file = repo_root / md_relative_path

    # If the file exists and feedback is provided, we edit.
    if md_target_file.exists() and feedback:
        logger.info(f"Reading existing draft for {topic} to apply feedback.")
        existing_content = md_target_file.read_text(encoding='utf-8')
        prompt = f"Edit the following essay about {topic} based on this feedback: {feedback}\n\nExisting Essay:\n{existing_content}"
    else:
        logger.info(f"Drafting new essay for {topic}.")
        prompt = ESSAY_TOOL_PROMPT + f"\nTopic: {topic}\nLength: {length}"

    logger.info("Calling essay LLM")
    response = get_llm_service().call_agent(prompt=prompt)
    logger.info("Response generated from essay LLM")

    md_content = response
    if not md_content.strip():
        raise RuntimeError("Essay LLM returned empty content")

    # Save the Markdown draft
    md_target_file.parent.mkdir(parents=True, exist_ok=True)
    md_target_file.write_text(md_content, encoding='utf-8')

    # Return the content to the agent so it can be sent back to Telegram
    return f"Draft saved to {md_target_file}. Here is a preview:\n\n{md_content}\n\nAsk the user if they approve or if they have feedback to change it."

@needle.tool
def finalize_and_publish_essay(topic: str):
    """
    Call this tool ONLY when the user explicitly approves the essay draft.
    It reads the approved Markdown file, generates a PDF, and prepares it for pushing.
    """
    repo_root = Path.cwd().resolve()
    md_relative_path = f"llm_gens/{topic}.md"
    pdf_relative_path = f"llm_gens/{topic}.pdf"
    
    md_target_file = repo_root / md_relative_path
    pdf_target_file = repo_root / pdf_relative_path

    if not md_target_file.exists():
        return f"Error: No markdown draft found for topic '{topic}'. You must draft it first."

    md_content = md_target_file.read_text(encoding='utf-8')

    try:
        pdf_bytes = _markdown_to_pdf_bytes(md_content)
        temporary_pdf_file = pdf_target_file.with_suffix(".pdf.tmp")
        temporary_pdf_file.write_bytes(pdf_bytes)
        temporary_pdf_file.replace(pdf_target_file)
    except Exception as e:
        logger.exception("PDF generation failed for topic %r: %s", topic, e)
        return {"response": f"Encountered an error creating the PDF for {topic}."}

    # TODO: Add your git commit and push logic here if you want it automated, 
    # or return success so the user knows they can push it manually.
    
    logger.info(f"Generated PDF to {pdf_target_file}")
    return {"response": f"Success! PDF generated at {pdf_target_file} and ready to be pushed to the repository."}

TOOLS = [draft_or_edit_essay, finalize_and_publish_essay]