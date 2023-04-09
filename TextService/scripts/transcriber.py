import whisper
import config

model = whisper.load_model(config.MODEL_WHISPER_SIZE, device="cpu")

def transcribe(audio):
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    detected_language = max(probs, key=probs.get)
    result = model.transcribe(audio)
    text = result["text"]
    return detected_language, text