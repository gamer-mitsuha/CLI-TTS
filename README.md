# CLI-TTS

A CLI app for Text to Speech (TTS).

## Set up environment

1. `git clone https://github.com/gamer-mitsuha/CLI-TTS.git`

1. Follow the instructions at [Azure's "Quickstart: Convert text to speech"](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?source=recommendations&tabs=windows%2Cterminal&pivots=programming-language-python).
    - Note that you need to set `SPEECH_KEY` and `SPEECH_REGION` environment variables on your OS.
    - An Azure account is required, however, each account has [0.5 million characters free quota per month](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/).

1. Install python libraries. Of course you can (or should) do this in a virtual env.

```py
pip install azure-cognitiveservices-speech "typer[all]"
```

(I decided to use Azure Cognitive Services after comparing Japanese female voices available for different cloud APIs :stuck_out_tongue_closed_eyes:)

## Usage

```py
python tts.py "your text input in Japanese" --output "your output file path"
```

Example:

```py
python tts.py "私に料理を作らせないでください。基本的に私はなんでもできますが、料理だけは本当にだめなんです…" --output "test.wav"
```
