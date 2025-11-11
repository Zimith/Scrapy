from deep_translator import GoogleTranslator
traductor = GoogleTranslator(source="auto", target="en") # traduce español a inglés para comparar


def traducir_palabra(palabra):
    try:
        return traductor.translate(palabra)
    except:
        return palabra
