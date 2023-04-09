from googletrans import Translator

translator = Translator()

def translate(text, dest='en'):
    translation = translator.translate(text, dest=dest)
    return translation.text, translation.src, translation.dest