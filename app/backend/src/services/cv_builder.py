import sys
from pathlib import Path

# Fix path resolution to match your project architecture
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from playwright.sync_api import sync_playwright
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import CVContentResponse, CVImprovementResponse

def _convert_html_to_pdf(html_path: Path, pdf_path: Path):
    """
    Renders the local HTML file using a headless browser and compiles it to a clean A4 PDF.
    """
    print(f"Compiling PDF print canvas via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Load the local HTML file via absolute file URI
        page.goto(f"file:///{html_path.resolve()}")
        
        # Emulate print media style to enforce professional margins and remove browser headers/footers
        page.emulate_media(media="print")
        
        # Generate A4 PDF with standard margins
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"}
        )
        browser.close()

def generate_improved_cv(cv_file: str, jd_text: str, output_html_path: str) -> CVImprovementResponse:
    """
    Executes a two-step sequential pipeline:
    Phase 1: Optimizes semantic text content against the JD.
    Phase 2: Generates a beautiful HTML/CSS file and builds a matching PDF asset.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt_engine = Prompt()
    
    # -------------------------------------------------------------------------
    # PHASE 1: Content Optimization Loop
    # -------------------------------------------------------------------------
    print("Executing Phase 1: Extracting and optimizing text context...")
    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    
    phase_1_prompt = prompt_engine.cv_content_optimizer(cv_text=cv_text, job_description=jd_text)
    
    phase_1_response = client.responses.parse(
        model=settings.OPENAI_MODEL_CV_IMPROVEMENT,
        max_output_tokens=settings.MAXIMUM_TOKENS_CV_IMPROVEMENT,
        prompt_cache_retention=settings.PROMPT_CACHE_RETENTION_CV_IMPROVEMENT,
        reasoning=settings.REASONING_EFFORT_CV_IMPROVEMENT,
        input=[{"role": "user", "content": [{"type": "input_text", "text": phase_1_prompt}]}],
        text_format=CVContentResponse,
    )
    
    content_data = phase_1_response.output_parsed
    if not content_data or not content_data.optimized_markdown:
        raise ValueError("Phase 1 failed: Could not generate optimized text payload.")
        
    print("Phase 1 Complete. Text optimization locked in.")

    # -------------------------------------------------------------------------
    # PHASE 2: HTML/CSS Code Rendering Loop
    # -------------------------------------------------------------------------

    print("Executing Phase 2: Generating responsive HTML and structural CSS...")
    phase_2_prompt = prompt_engine.cv_html_renderer(optimized_markdown=content_data.optimized_markdown)
    
    phase_2_response = client.responses.parse(
        model=settings.OPENAI_MODEL_CV_IMPROVEMENT,
        max_output_tokens=settings.MAXIMUM_TOKENS_CV_IMPROVEMENT,
        prompt_cache_retention=settings.PROMPT_CACHE_RETENTION_CV_IMPROVEMENT,
        reasoning=settings.REASONING_EFFORT_CV_IMPROVEMENT,
        input=[{"role": "user", "content": [{"type": "input_text", "text": phase_2_prompt}]}],
        text_format=CVImprovementResponse,
    )
    
    html_data = phase_2_response.output_parsed
    if not html_data or not html_data.optimized_html:
        raise ValueError("Phase 2 failed: Could not generate final HTML canvas code.")

    # -------------------------------------------------------------------------
    # IO WRITE: Save both HTML and PDF formats safely to disk
    # -------------------------------------------------------------------------
    html_file = Path(output_html_path)
    html_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Write HTML File
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_data.optimized_html)
    print(f"HTML CV successfully saved to: {html_file}")

    # 2. Derive PDF Path and Write PDF File
    pdf_file = html_file.with_suffix(".pdf")
    try:
        _convert_html_to_pdf(html_path=html_file, pdf_path=pdf_file)
        print(f"PDF CV successfully saved to: {pdf_file}")
    except Exception as pdf_error:
        print(f"Warning: HTML saved, but PDF generation encountered an error: {pdf_error}")

    print(f"\nPipeline complete! Dual assets generated inside: {html_file.parent}")
    return html_data


if __name__ == "__main__":
    cv_path = r"C:\files\mrmayd\app\backend\files\Anon Hossain AI.docx.pdf"
    save_path = r"C:\files\mrmayd\app\backend\output\new_CV.html"
    job_description_path = r"C:\files\mrmayd\app\backend\Dumy.txt"

    with open(job_description_path, "r", encoding="utf-8") as file:
        job_description_text = file.read()

    if Path(cv_path).exists():
        generate_improved_cv(
            cv_file=cv_path,
            jd_text=job_description_text,
            output_html_path=save_path
        )