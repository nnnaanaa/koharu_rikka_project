import sounddevice as sd
import soundfile as sf

filename = "./data/hello_v1.wav"  # 修正: Windows の `\` ではなく Linux の `/` を使う
data, samplerate = sf.read(filename)
sd.play(data, samplerate)
sd.wait()
