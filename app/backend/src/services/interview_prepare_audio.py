import sys
import json
from pathlib import Path

# Fix path resolution to match your project architecture
sys.path.append(str(Path(__file__).resolve().parents[1]))

from schemas.models import InterviewQAEntry
from module.stt import STTService

def process_and_save_interview_audio_entry(
    question: str, 
    answer: str, 
    response_input: str, 
    output_json_path: str
):
    """
    Accepts an audio file path (.mp3), transcribes it to text using STTService,
    validates the data via Pydantic, and appends it to the target interview JSON file.
    """
    # 1. Initialize the STT Service and transcribe the audio file to text
    stt_service = STTService()
    print(f"Processing audio response for question: '{question[:30]}...'")
    transcribed_text = stt_service.transcribe_audio(response_input)
    
    # 2. Structure data using the static Pydantic model
    qa_entry = InterviewQAEntry(
        question=question,
        answer=answer,
        response=transcribed_text
    )
    
    output_file = Path(output_json_path)
    # 3. Automatically create the directory path if it doesn't exist yet
    output_file.parent.mkdir(parents=True, exist_ok=True)
    current_entries = []
    
    # 4. Check if file exists and has content to append to
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

    # 5. Append the new validated text entry
    current_entries.append(qa_entry.model_dump())

    # 6. Save the updated list back to the target JSON file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(current_entries, file, indent=4)

    print(f"Successfully updated: {output_json_path} (Total entries: {len(current_entries)})\n")


if __name__ == "__main__":
    target_json = "C:\\files\\mrmayd\\app\\backend\\output\\interview.json"
    # Notice: NO trailing commas here! Pure strings.
    question = "Why Are you here?"
    answer = "Candidate should know basic syntax and OOP principles."
    audio_response_path = "C:\\files\\mrmayd\\app\\backend\\files\\Recording.mp3"
    
    process_and_save_interview_audio_entry(
        question=question,
        answer=answer,
        response_input=audio_response_path,
        output_json_path=target_json
    )