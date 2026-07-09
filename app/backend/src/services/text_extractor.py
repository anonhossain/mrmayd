#app/backend/src/text_extractor.py

import base64
import io
import fitz
from PIL import Image
from openai import OpenAI
from core.config import settings
from prompts.prompt import Prompt


class TextExtractor:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_VISION_MODEL
        self.dpi = settings.PDF_RENDER_DPI

    ########################################################################
    # Main Function
    ########################################################################

    def extract_text(self, cv_path: str) -> str:
        """
        Main orchestration function.
        """

        cv_txt = self.manual_extraction(cv_path)

        if cv_txt.strip():
            print("Embedded text found.")
            return cv_txt

        print("No embedded text found. Switching to OCR...")

        cv_txt = self.ocr_extraction(cv_path)

        return cv_txt

    ########################################################################
    # Manual Extraction (PyMuPDF)
    ########################################################################

    def manual_extraction(self, cv_path: str) -> str:

        doc = fitz.open(cv_path)

        pages = []

        for page in doc:

            text = page.get_text("text")

            if text:
                pages.append(text)

        doc.close()

        cv_txt = "\n".join(pages).strip()

        return cv_txt

    ########################################################################
    # OCR Extraction (GPT-5 Vision)
    ########################################################################

    # def ocr_extraction(self, cv_path: str) -> str:

    #     doc = fitz.open(cv_path)

    #     zoom = self.dpi / 72
    #     matrix = fitz.Matrix(zoom, zoom)

    #     extracted_pages = []

    #     for page_number, page in enumerate(doc, start=1):

    #         pix = page.get_pixmap(matrix=matrix)

    #         image = Image.frombytes(
    #             "RGB",
    #             [pix.width, pix.height],
    #             pix.samples,
    #         )

    #         buffer = io.BytesIO()

    #         image.save(buffer, format="PNG")

    #         image_b64 = base64.b64encode(
    #             buffer.getvalue()
    #         ).decode()

    #         response = self.client.responses.create(

    #             model=self.model,

    #             input=[
    #                 {
    #                     "role": "user",
    #                     "content": [

    #                         {
    #                             "type": "input_text",
    #                             "text": Prompt().extraction()
    #                         },

    #                         {
    #                             "type": "input_image",
    #                             "image_url": f"data:image/png;base64,{image_b64}",
    #                         },
    #                     ],
    #                 }
    #             ],
    #         )

    #         page_text = response.output_text.strip()

    #         extracted_pages.append(page_text)

    #         print(f"Finished OCR Page {page_number}")

    #     doc.close()

    #     cv_txt = "\n\n".join(extracted_pages)

    #     return cv_txt