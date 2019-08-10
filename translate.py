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
			
		elif sentence.startswith("You have entered an invalid symbol"):
			return "Gecersiz kisaltma girdiniz"
		
		elif "Change(24 hrs)" in sentence:
			return " Degisim(24 saat): %"

		elif "Price" in sentence:
			return " Fiyat: "
