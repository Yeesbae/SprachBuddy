from gtts import gTTS
import io

def text_to_speech(text: str, lang: str = 'de') -> io.BytesIO:
    """
    Convert text to speech and return as a BytesIO object.
    
    Args:
        text: The text to convert to speech
        lang: The language for the TTS conversion (default is English)
    """
    tts = gTTS(text=text, lang=lang)
    voice_bytes = io.BytesIO()
    tts.write_to_fp(voice_bytes)
    voice_bytes.seek(0)  # Reset pointer to the start of the BytesIO object
    return voice_bytes
