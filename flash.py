# flashcard
import subprocess
import numpy as np
import whisper
import ffmpeg
import yt_dlp

def transcribe_youtube(url, model_size="base"):
    """
    Transcribes a YouTube video into text with timestamps using Whisper.
    Returns list of segments: {start, end, text}.
    """

    # Load Whisper model
    model = whisper.load_model(model_size)

    # ---- Get direct audio URL (avoid 403 errors) ----
    ydl_opts = {"format": "bestaudio/best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info["url"]

    # ---- Stream audio via ffmpeg ----
    out, _ = (
        ffmpeg
        .input(audio_url)
        .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar="16000")
        .run(capture_stdout=True, capture_stderr=True)
    )

    # Convert raw bytes → NumPy float32
    audio = np.frombuffer(out, np.int16).astype(np.float32) / 32768.0
def generate_flashcards(segments):
    """
    Create flashcards from transcript segments.
    Each card = {question, answer}.
    """
    flashcards = []
    for seg in segments:
        text = seg["text"].strip()

        # Question based on timestamps
        q = f"What happens between {seg['start']:.2f}s and {seg['end']:.2f}s?"
        a = text

        flashcards.append({"question": q, "answer": a})
    return flashcards
    return result["segments"]
    