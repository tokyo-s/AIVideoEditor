from deep_translator import GoogleTranslator

def translate(text, target='en'):
    translator = GoogleTranslator(source='auto', target=target)
    translated = translator.translate(text) 
    return translated

def translate_subtitles(subtitles, target='en'):
    translator = GoogleTranslator(source='auto', target=target)
    for sub in subtitles:
        sub['text'] = translator.translate(sub['text']) 
    return subtitles