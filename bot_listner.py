import pyaudio
import wave
import io
from google.cloud import speech_v1 as speech
import sounddevice as sd

# Googleクラウドの認証情報を設定する
# この部分は環境に合わせて変更が必要
speech_client = speech.SpeechClient.from_service_account_json('ここにGCPの認証ファイルのパスを記載する')


def speech2text():
    # マイクからの入力を設定する
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #RATE = 16000
    RECORD_SECONDS = 10
    
    # 入力デバイス情報に基づき、サンプリング周波数の情報を取得
    input_device_info = sd.query_devices(kind="input")
    RATE = int(input_device_info["default_samplerate"])

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("音声入力中...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("音声入力が終了しました。")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wavefile = io.BytesIO()
    wavefileobject = wave.open(wavefile, 'wb')
    wavefileobject.setnchannels(CHANNELS)
    wavefileobject.setsampwidth(p.get_sample_size(FORMAT))
    wavefileobject.setframerate(RATE)
    wavefileobject.writeframes(b"".join(frames))
    wavefileobject.close()

    # Google Cloud Speech-to-Textを使って音声を文字起こしする
    audio = speech.RecognitionAudio(content=wavefile.getvalue())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="ja-JP",
    )

    response = speech_client.recognize(config=config, audio=audio)

    result_text = ""

    # 認識した文字列を出力する
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        result_text += result.alternatives[0].transcript

    return result_text

if __name__ == "__main__":
    result_text = speech2text()
