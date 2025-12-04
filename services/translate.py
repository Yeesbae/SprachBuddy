from googletrans import Translator
from deep_translator import GoogleTranslator

translator = Translator()

async def google_trans(text, target_lang):
    result = await translator.translate(text, dest=target_lang)
    return result.text


def deep_trans(text, target_lang):
    return GoogleTranslator(source='auto', target=target_lang).translate(text)
