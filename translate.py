"""


Translate Turkish bot messages to English according to user's language code


"""


def translate(sentence, language_code):
	
	if "tr" in language_code:
		return sentence
	
	else:
		if sentence.startswith("Merhaba "):
			return "Hello "
		
		elif sentence.startswith("Bir hata olustu"):
			return "An error has occurred"
			
		elif sentence.startswith("Gecersiz kisaltma girdiniz"):
			return "You have entered an invalid symbol"
		
		elif "Degisim(24 saat)" in sentence:
			return " Change(24 hrs): %"

		elif "Fiyat" in sentence:
			return " Price: "
