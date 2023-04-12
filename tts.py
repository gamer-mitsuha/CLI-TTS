"""Simple command line interface for text to speech.

Using the Azure Cognitive Services Speech SDK for Python.
See https://bit.ly/3MCvcEj for the environment setup.

Example usage:
  python tts.py "こんにちは。私はPythonです。" --output output.wav
"""

import os

import azure.cognitiveservices.speech as speechsdk
import typer

app = typer.Typer()

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION")
)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name = "ja-JP-NanamiNeural"

@app.command()
def tts(text: str, output: str = "output/sample.wav"):
    """Simple command line interface for text to speech."""
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    speech_synthesizer.speak_text_async(text).get()


if __name__ == "__main__":
    app()
