# import whisper
import config
import whisper_timestamped as whisper

model = whisper.load_model(config.MODEL_WHISPER_SIZE, device=config.DEVICE)

# result = whisper_timestamped.transcribe(audio=audio_file, model=model)
def audio_to_text(audio):
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    detected_language = max(probs, key=probs.get)
    result = model.transcribe(audio, language="en")

    text = result["text"]
    return text, result
