import sys
import json
from pathlib import Path

# Fix path resolution to match your project architecture
sys.path.append(str(Path(__file__).resolve().parents[1]))

from schemas.models import InterviewQAEntry

def process_and_save_interview_entry(
    question: str, 
    answer: str, 
    response_input: str, 
    output_json_path: str = "app/backend/output/interview.json"
):
    """
    Accepts string text inputs, validates them using the Pydantic schema, 
    and appends them to the target interview JSON file. Creates the folder 
    and file dynamically if they do not exist.
    """
    
    # 1. Structure data using the static Pydantic model
    qa_entry = InterviewQAEntry(
        question=question,
        answer=answer,
        response=response_input
    )
    
    output_file = Path(output_json_path)
    
    # 2. Automatically create the directory path if it doesn't exist yet
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    current_entries = []
    
    # 3. Check if file exists and has content to append to
    if output_file.exists() and output_file.stat().st_size > 0:
        try:
            with open(output_file, "r", encoding="utf-8") as file:
                current_entries = json.load(file)
                # Ensure the loaded data is a list structure
                if not isinstance(current_entries, list):
                    current_entries = []
        except json.JSONDecodeError:
            # Fallback if the file is corrupted
            current_entries = []

    # 4. Append the new validated text entry
    current_entries.append(qa_entry.model_dump())

    # 5. Save the updated list back to the target JSON file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(current_entries, file, indent=4)

    print(f"Successfully updated: {output_json_path} (Total entries: {len(current_entries)})")


if __name__ == "__main__":
    target_json = "C:\\files\\mrmayd\\app\\backend\\output\\interview.json"
    
    # Notice: NO trailing commas here!
    question = "Why Are you here?"
    answer = "Candidate should know basic syntax and OOP principles."
    response_input = "I have built data pipelines and backend applications using Python for 3 years."
    
    process_and_save_interview_entry(
        question=question,
        answer=answer,
        response_input=response_input,
        output_json_path=target_json
    )