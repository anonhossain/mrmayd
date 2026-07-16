## System Architecture Class Diagram

```mermaid
classDiagram
    direction TB

    class Settings {
        +str OPENAI_API_KEY
        +str OPENAI_MODEL_CV_IMPROVEMENT
        +str OPENAI_MODEL_SUGGESTIONS
        +int MAXIMUM_TOKENS_CV_IMPROVEMENT
        +int MAXIMUM_TOKENS_SUGGESTIONS
        +float TEMPERATURE_SUGGESTIONS
        +str REASONING_EFFORT_CV_IMPROVEMENT
    }

    class TextExtractor {
        +extract_text(cv_file: str) str
    }

    class Prompt {
        +cover_letter(jd_text: str, cv_text: str) str
        +cv_improver(cv_text: str, job_description: str) str
        +cv_content_optimizer(cv_text: str, job_description: str) str
        +cv_html_renderer(optimized_markdown: str) str
        +suggestion(cv_text: str) str
    }

    class CoverLetter {
        +str content
    }

    class CVContentResponse {
        +str optimized_markdown
    }

    class CVImprovementResponse {
        +str optimized_html
    }

    class Suggestions {
        +list recommendations
    }

    class InputGuardrail {
        +validate_cv_and_jd(cv_text: str, jd_text: str) bool
    }

    class OutputGuardrail {
        +verify_content_fidelity(original_cv: str, optimized_markdown: str) bool
        +verify_html_safety(html_content: str) bool
    }

    class CVBuilderService {
        +generate_improved_cv(cv_file: str, jd_text: str, output_html_path: str) CVImprovementResponse
        -_convert_html_to_pdf(html_path: Path, pdf_path: Path) void
    }

    class SuggestionsService {
        +suggestions(cv_file: str) Suggestions
    }

    class OpenAIClient {
        +responses.parse()
    }

    class PlaywrightPDFEngine {
        +page.pdf()
    }

    class LogfireTelemetry {
        +configure()
        +instrument_openai()
        +instrument()
    }

    %% Relationships & Dependencies
    CVBuilderService --> TextExtractor : Uses
    CVBuilderService --> Prompt : Builds Prompts
    CVBuilderService --> Settings : Reads Config
    CVBuilderService --> InputGuardrail : Validates Inputs
    CVBuilderService --> OutputGuardrail : Verifies Outputs
    CVBuilderService --> OpenAIClient : Executes Calls
    CVBuilderService --> PlaywrightPDFEngine : Renders PDF
    CVBuilderService --> LogfireTelemetry : Traces Execution
    CVBuilderService ..> CVContentResponse : Parses Phase 1
    CVBuilderService ..> CVImprovementResponse : Parses Phase 2

    SuggestionsService --> TextExtractor : Uses
    SuggestionsService --> Prompt : Builds Prompts
    SuggestionsService --> Settings : Reads Config
    SuggestionsService --> OpenAIClient : Executes Calls
    SuggestionsService --> LogfireTelemetry : Traces Execution
    SuggestionsService ..> Suggestions : Parses Output
