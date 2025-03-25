# ai_config.py
from io import BytesIO
from langchain_openai import ChatOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Model configuration
model = "gpt-4o-mini"

# Load the OpenAI model for text generation
def load_model(openai_api_key):
    return ChatOpenAI(
        model_name=model,
        openai_api_key=openai_api_key,
        temperature=0.5
    )

# Initialize the OpenAI client for speech and transcription
client = OpenAI(api_key=openai_api_key)

# Convert text to speech
def convert_text_to_speech(text, output, voice="alloy"):
    """
    Convert text to speech using OpenAI's TTS API.
    Args:
        text (str): The text to convert to speech.
        output: Either a file path (str) or BytesIO object to write the audio to.
        voice (str): The voice to use (e.g., 'alloy', 'onyx').
    """
    try:
        response = client.audio.speech.create(model="tts-1-hd", voice=voice, input=text)
        
        if isinstance(output, BytesIO):
            # Write to BytesIO buffer
            for chunk in response.iter_bytes():
                output.write(chunk)
        else:
            # Write to file path
            with open(output, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
        # Fallback to a default message
        fallback_text = "An error occurred while generating audio."
        response = client.audio.speech.create(model="tts-1-hd", voice=voice, input=fallback_text)
        if isinstance(output, BytesIO):
            for chunk in response.iter_bytes():
                output.write(chunk)
        else:
            with open(output, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

# Transcribe audio to text
def transcribe_audio(audio):
    """
    Transcribe audio file to text using OpenAI's Whisper API.
    Args:
        audio (str): Path to the audio file.
    Returns:
        str: Transcribed text.
    """
    try:
        with open(audio, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text
    except Exception as e:
        print(f"Error in audio transcription: {e}")
        return "Error transcribing audio."
