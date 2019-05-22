"""Spell Check Module."""
from prodigyqa import BrowserActions
import re
import nltk
import aspell
import string

nltk.download('punkt')


class SpellChecker(BrowserActions):
    """Spell Checker with Custom Libraries."""

    def spell_check_on_page(self, url, words=[]):
        """Spell checker.

        :param url: webpage url
        :param words: expected word list
        :return: list of misspelled words
        TODO: Expand the parameter of words into txt/csv/custom string.
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
                               for word in cleantext if not
                               speller_obj.check(
            word) and re.match('^[a-zA-Z ]*$', word)]))
        return misspelled
