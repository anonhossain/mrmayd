import sys
from pathlib import Path
from openai import OpenAI

# Fix path resolution to match your project architecture hierarchy
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.config import settings

class STTService:
    def __init__(self):
        """
        Initializes the Speech-to-Text service with the configured OpenAI client.
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_STT_MODEL

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Takes an MP3 file path, validates its existence, and uses the 
        OpenAI API to transcribe the audio content into text.
        """
        audio_path = Path(audio_file_path)
        
        # Defensive check to validate file presence before calling external APIs
        if not audio_path.is_file():
            raise FileNotFoundError(f"Target audio file does not exist at: {audio_file_path}")
            
        print(f"[STTService] Dispatching {audio_path.name} to OpenAI pipeline...")
        
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )
        
        return transcription.text
    


if __name__ == "__main__":
    # Example usage
    stt_service = STTService()
    audio_file_path = r"C:\files\mrmayd\app\backend\files\Recording.mp3" 
    transcript = stt_service.transcribe_audio(audio_file_path)
    print(transcript)
    