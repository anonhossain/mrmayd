from pydantic import BaseModel, Field
from typing import List, Optional

class CoverLetter(BaseModel):
    subject: str = Field(description="Proper subject like applying {company_name} as {position}")
    body: str = Field(description="The full body of the letter, No need to include footer info like Regards or Sincerely and {name} extracted from CV .")
    footer: str = Field(description="The footer contains Regards or Sincerely and {name} extracted from CV.")

class Suggestions(BaseModel):
    skills: str = Field(description="List of all skills present in the CV")
    suggestions: str = Field(description="Suggestions to improve the CV, including skills that can be added to make it more relevant and standard.")

class Matcher(BaseModel):
    match_score: float = Field(description="The percentage match between the CV and the job description")

class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question generated based on the CV and job description")
    answer: str = Field(description="The answer to the interview question, based on the CV and job description")

class InterviewQuestionsResponse(BaseModel):
    questions: List[InterviewQuestion] = Field(
        description="A list containing the exact number of generated interview questions and answers"
    )

class InterviewEvaluation(BaseModel):
    question: str = Field(description="The original interview question asked to the candidate") 
    #CHANGE THIS DESCRIPTION:
    answer: str = Field(description="The ideal or expected answer for this question")
    response: str = Field(description="The actual response provided by the candidate")
    score: int = Field(
        description="The performance score assigned to the response on a scale of 1 to 10", 
        ge=1, 
        le=10
    )

class InterviewEvaluationsResponse(BaseModel):
    evaluations: List[InterviewEvaluation] = Field(
        description="A list containing the full evaluations for each interview question"
    )

class InterviewQAEntry(BaseModel):
    question: str
    answer: str
    response: str

class CVContentResponse(BaseModel):
    optimized_markdown: str = Field(
        description="The completely rewritten and optimized CV content in markdown format, perfectly aligned with the JD keywords."
    )

class CVImprovementResponse(BaseModel):
    optimized_html: str = Field(
        description="The complete, production-grade HTML5 document containing all CV sections with embedded CSS styling within the <head>."
    )