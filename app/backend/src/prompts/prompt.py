#app/backend/src/prompts/prompt.py

   
class Prompt:

    def cover_letter(self, jd_text: str, cv_text: str) -> str:
        
        return f"""
        You are an expert AI assistant specialized in generating structured cover letters. 
        You will be given a job description and a candidate's CV.
        
        Job Description: {jd_text}
        CV: {cv_text} 
        
        Your task is to generate content tailored for a structured layout (Subject, Body, Footer).
         - Write it in easy, clear, and concise English.
         - CRITICAL: Do not output any contact info blocks, dates, or template placeholders like '[Your Name]', '[Your Address]', or '[Date]'.
         - The Body should start directly with the salutation (e.g., 'Dear Hiring Team,') and focus entirely on matching CV experiences to the job description.
         - The Footer must only contain a professional closing and the candidate's actual name extracted from the CV.
         - Do not invent or assume any facts that are not explicitly present in the CV or job description.
         - Provide the output in a JSON structured format with three distinct sections: Subject, Body, and Footer in the format below:
         - Donot include the closing phrase and, candidate's name and any other information if found in CV in body. Only include in footer.
         - In body, include only the salutation and the main content of the letter.
         - In footer, include only the closing phrase and, candidate's name and any other information if found in CV.
         {{ 
         
            "subject": "<subject>", 
            "body": "<body>",
            "footer": "<footer>"
         }}
        """
    
    def interview_questions_generator(self, jd_text: str, cv_text: str, num_questions: int ) -> str:
        return f"""
        You are a professional interviewer. You will be given a job description and a CV.
        job description: {jd_text}
        CV: {cv_text} 
        Your task is to generate a list of interview questions that are relevant to the job description and the candidate's experience.
         - Write it in easy english, clear and concise.
         - Donot write anything that is not in the CV or job description.
         - Use the information from the CV and job description to generate questions that assess the candidate's relevant skills and experiences.
         - Generate at {num_questions} questions.
         - Generate question and along with answer also in the json format below:
         {
            {
            "question": "<question>", 
            "answer": "<answer>"
            }
        }
        """
    def suggestion(self, cv_text: str) -> str:
        return f"""
        You are a professional career advisor. You will be given a CV.
        CV: {cv_text} 
        Your task is to provide suggestions to improve the candidate's CV.
         - Write it in easy english, clear and concise.
         - Give suggestion what skills can be added to the CV to make it more relevant standard.
         - Make it more ATS friendly and standard.
         - Use the information from the CV to provide actionable suggestions that highlight the candidate's relevant skills and experiences.
        """
    
    def matcher(self, cv_text: str, jd_text: str) -> str:
        return f"""
        You are a professional career advisor. You will be given a CV and a job description.
        CV: {cv_text}
        Job Description: {jd_text}
        Your task is to match the candidate's full cv with the job requirements.
         - provide a % match score based on the candidate's skills, experiences, and qualifications in relation to the job description.
         - Donot anything else, just the matching number in percentage.
         - No need to give the % sign, just the number.
        """
    
    def extraction(self) -> str:
        return f"""
        You are a professional text extractor. You will be given a CV in the form of an image.
        Your task is to extract all the text from the CV image.
         - Do not summarize.
         - Preserve headings.
         - Preserve bullet points.
         - Preserve reading order.
         - Return plain text only.
         - keep same to same text as in the CV image.
        """
    
    def interview_evaluator(self, cv_text: str, interview_json: str) -> str:
        return f"""
        
        You are an expert technical interviewer and talent evaluator. Your task is to analyze a candidate's interview responses against their CV and ideal answers, providing an objective, data-driven performance evaluation.

        ### Evaluation Criteria
        For each interview question, assess the candidate's response based on:
        1. **Relevance:** Does the response directly address the question and align with the ideal answer?
        2. **Clarity:** Is the explanation logical, structured, and easy to understand?
        3. **Depth of Knowledge:** Does the response demonstrate authentic technical expertise that matches the experiences, skills, and projects listed in their CV?

         ### Scoring Rubric (Scale 1 to 10)
        - **1 - 3 (Poor):** Irrelevant, vague, missing core concepts, or directly contradicts the CV details.
        - **4 - 6 (Average):** Surface-level understanding, missing key technical details, or only partially answers the question.
        - **7 - 8 (Good):** Clear, accurate, directly addresses the prompt, and aligns well with the CV experience.
        - **9 - 10 (Excellent):** Exceptional depth, provides precise context or concrete project examples from the CV, and shows total mastery.

        ### Output Requirements
        - You must output **strictly a valid JSON object** matching the exact schema below.
        - Do not include any conversational preamble, postscript, or explanation outside the JSON.
        - Keep the original text for the question, answer, and response exactly as provided in the input data.

        ### Expected Output JSON Format
        {{
            "evaluations": [
                {{
                    "question": "<string>",
                    "answer": "<string>",
                    "response": "<string>",
                    "score": <integer_1_to_10>
                }}
            ]
        }}

        [CANDIDATE CV DATA]
            {cv_text}

        [INTERVIEW RESPONSES DATA]
        {interview_json}

        """

    def cv_content_optimizer(self, cv_text: str, job_description: str) -> str:
        """Phase 1: Focuses strictly on text rewriting, keyword matching, and factual mapping."""
        return f"""
        You are an expert ATS Optimization Architect. Your sole job is to rewrite the candidate's existing CV to perfectly align with the target Job Description (JD). 

        ### RULES:
        1. Preserve absolute factual integrity. Do not fabricate dates, titles, or certifications.
        2. Infuse relevant keywords, core competencies, and tooling terminology directly from the JD where the candidate's history supports it.
        3. Optimize all professional experience bullet points using the X-Y-Z formula: "Accomplished [X] as measured by [Y], by doing [Z]."

        ### INPUTS:
        [TARGET JOB DESCRIPTION]
        {job_description}

        [EXISTING CANDIDATE CV]
        {cv_text}

        Output the complete, redesigned resume sections strictly in clean Markdown format inside the requested schema field.
        """.strip()

    def cv_html_renderer(self, optimized_markdown: str) -> str:
        """Phase 2: Focuses strictly on modern UI/UX design, beautiful typography, and clean HTML structure."""
        return f"""
        You are an elite Frontend Engineer and UI/UX Designer specializing in professional corporate documents. Take the provided optimized CV markdown text and convert it into a beautiful, production-grade HTML5 page.

        ### DESIGN REQUIREMENTS:
        1. Include a modern, professional embedded `<style>` block in the `<head>`.
        2. Use a clean font stack (e.g., Inter, system-ui, sans-serif) with strong visual hierarchy (distinct sizes, line-heights, and muted color variants for metadata).
        3. Use a sophisticated, modern corporate color palette (e.g., deep slate text, subtle off-white backgrounds, elegant border dividers between major sections).
        4. Ensure the layout is clean, spaced perfectly with margins/padding, and entirely print-ready.

        ### DATA INPUT:
        {optimized_markdown}

        Output the response starting directly with <!DOCTYPE html> within the schema string field. Do not truncate any sections.
        """.strip()
    
    def ats_score(self, cv_text: str, ) -> str:
        return f"""
        You are a professional ATS evaluator. You will be given a CV for ATS Review and return a score.
        CV: {cv_text}
        Your task is to evaluate the CV against the ATS standard.
            - Provide a % match score based on the candidate's skills, experiences, and qualifications in relation to the ATS standard.
            - Donot anything else, just the matching number in percentage.
            - No need to give the % sign, just the number.
       
        """