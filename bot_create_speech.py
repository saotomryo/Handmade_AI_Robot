from google.cloud import texttospeech
import os
import sys
import pyaudio



def speech(speech_text):
    # Google Cloud 認証
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ここにGCPの認証ファイルのパスを記載する'

    # Instantiate a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=speech_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,speaking_rate=2
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=16000,
                    output=True)
    stream.write(response.audio_content)
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    speech("こんにちは、お話しましょう")
