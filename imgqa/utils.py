"""Image Comparison Module using Structural Similary and Open CV."""
from PIL import Image
import aspell
import pytesseract
from selenium import webdriver
import re
import string
import nltk
nltk.download('punkt')


class Utilities:
    """Extract the text from image presented."""

    def captcha_to_text(self, image):
        """Method to return extracted text from passed image."""
        return pytesseract.image_to_string(Image.open(image))

    def spell_checker(self, url, words=[]):
        """Spell checker.

        :param url:
        :param words: expected word list
        :return: list of misspelled words
        """
        speller_obj = aspell.Speller()
        if not words:
            for word in words:
                speller_obj.addtoSession(word)

        driver = webdriver.Chrome()
        driver.get(url)
        cleanr = re.compile('<.*?>')
        page_content = re.sub(cleanr, '', driver.page_source)
        invalidchars = set(string.punctuation.replace("_", "")) | {"\u"}

        cleantext = []
        for word in nltk.word_tokenize(page_content):
            if any(invalidchar in word
                   for invalidchar in invalidchars) or len(word) < 2:
                continue
            else:
                cleantext.append(word)

        misspelled = list(set([word.encode('ascii', 'ignore')
                               for word in cleantext
                               if not speller_obj.check(word) and
                               re.match('^[a-zA-Z ]*$', word)]))

        return misspelled
