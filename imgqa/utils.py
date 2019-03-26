"""Image Comparison Module using Structural Similary and Open CV."""
from PIL import Image
import aspell
import pytesseract
import re
import string
from imgqa import BrowserActions
import nltk
from axe_selenium_python import Axe

nltk.download('punkt')


class Utilities(BrowserActions):
    """Extract the text from image presented."""

    def captcha_to_text(self, image):
        """Method to return extracted text from passed image."""
        return pytesseract.image_to_string(Image.open(image))

    def spell_checker(self, url, words=[]):
        """Spell checker.

        :param url: webpage url
        :param words: expected word list
        :return: list of misspelled words
        """
        self.open(url)
        cleanr = re.compile('<.*?>')
        page_content = re.sub(cleanr, '', self.get_page_source())
        cleantext = []
        speller_obj = aspell.Speller("lang", "en")
        if len(words):
            for word in words:
                speller_obj.addtoSession(word)

        invalidchars = set(string.punctuation.replace("_", ""))
        for word in nltk.word_tokenize(page_content):
            if any(invalidchar in word for invalidchar in invalidchars) or \
                    len(word) < 2:
                continue
            else:
                cleantext.append(word)

        misspelled = list(set([word.encode('ascii', 'ignore')
                               for word in cleantext
                               if not speller_obj.check(word) and
                               re.match('^[a-zA-Z ]*$', word)]))

        return misspelled

    def accesibility_check(self, url):
        self.open(url)
        axe = Axe(self.driver)
        # Inject axe-core javascript into page.
        axe.inject()
        
        # Run axe accessibility checks.
        results = axe.run()
        
        # Write results to file
        axe.write_results(results, 'a11y.json')
        
        # Assert no violations are found
        assert len(results["violations"]) == 0, axe.report(results["violations"])   
