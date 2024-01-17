"""Simple command line interface for text to speech.

Using the Azure Cognitive Services Speech SDK for Python.
See https://bit.ly/3MCvcEj for the environment setup.

Example usage:
  python tts.py "こんにちは。私はPythonです。" --output output.wav
"""

import os
import shutil
import uuid

import azure.cognitiveservices.speech as speechsdk
import redis
import typer

app = typer.Typer()

pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
r = redis.Redis(connection_pool=pool)

DEFAULT_CACHE_DIR = "cache"


# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION")
)

# The language of the voice that speaks.
# speech_config.speech_synthesis_voice_name = "ja-JP-NanamiNeural"
# speech_config.speech_synthesis_voice_name = "ja-JP-KeitaNeural"
speech_config.speech_synthesis_voice_name = "ja-JP-NaokiNeural"


@app.command()
def tts(
    text: str, output: str = "output/sample.wav", cache_dir: str = DEFAULT_CACHE_DIR
):
    """Simple command line interface for text to speech."""

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Check if the synthesized speech of the input text is already in the cache.
    # Use the text and the voice name as the key.
    cache_key = speech_config.speech_synthesis_voice_name + ":" + text
    cache_path = r.get(cache_key)
    if cache_path is not None:
        print("Found in cache.")
        cache_path = cache_path.decode("utf-8")

        # Check if the cache is valid. If so, use it as the output.
        if os.path.exists(cache_path):
            print("Cache is valid.")
            # Copy the synthesized speech from the cache to the output path.
            shutil.copy(cache_path, output)
            return

        # Otherwise, delete the invalid cache.
        print("Cache is not valid.")
        r.delete(cache_key)
        print("Deleted invalid cache.")

    # If not found in cache or cache is invalid, synthesize the text and store it in the cache.
    print("Not found in cache. Synthesizing...")
    cache_path = os.path.join(cache_dir, f"{uuid.uuid4()}.wav")

    # Synthesize the text.
    audio_config = speechsdk.audio.AudioOutputConfig(filename=cache_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    speech_synthesizer.speak_text_async(text).get()

    # Cache the synthesized speech.
    r.set(cache_key, cache_path)

    # Copy the synthesized speech from the cache to the output path.
    shutil.copy(cache_path, output)


if __name__ == "__main__":
    app()
