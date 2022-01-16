"""
Translate Turkish bot messages to English according to user's language code
"""


def translate(sentence, language_code):

    if "en" in language_code:
        return sentence

    else:
        if sentence.startswith("Hello "):
            return "Merhaba "

        elif sentence.startswith("An error has occurred"):
            return "Bir hata olustu"

        elif "Price Time" in sentence:
            return "Fiyat Zamanı: "

        elif sentence.startswith("You have entered an invalid symbol"):
            return "Gecersiz kisaltma girdiniz"

        elif "Change" in sentence:
            return " Degisim: %"

        elif "Price" in sentence:
            return " Fiyat: "

        elif "Hi!" in sentence:
            return "Merhaba! Yardım için /help yazabilirsin"

        elif "Simply" in sentence:
            return "Coin ismini yazarak fiyat bilgisine erişebilirsin. BTC, ETH, DOT gibi. Büyük-küçük harf önemsiz"
