import unittest, math
from words import load_letter_frequencies, load_word_list, WordProbability, Letters


class TestWords(unittest.TestCase):
    def test_load_letter_frequencies(self):
        wordlist = load_letter_frequencies("english_monograms.txt")
        self.assertEqual(len(wordlist), 26)
        self.assertAlmostEqual(sum(math.exp(v) for v in wordlist.values()), 1.0, 10)

    def test_word_score(self):
        word_list = load_word_list("wordlist.txt")
        frequencies = [load_letter_frequencies("english_monograms.txt"),
                       load_letter_frequencies("english_bigrams.txt"),
                       load_letter_frequencies("english_trigrams.txt")]
        wp = WordProbability(frequencies)
        scores = {word: wp.word_rank_score(word) for word in word_list if len(word) == 5}
        l = list(sorted(scores, key=scores.get, reverse=True))
        self.assertEqual(l[0], 'ATONE')

    def test_letters_initally_all_valid(self):
        letters = Letters(5)
        for letter in letters.alphabet:
            for location in range(5):
                self.assertTrue(letters.is_valid_in_location(letter, location))

    def test_invalid_in_location(self):
        letters = Letters(5)
        letters.mark_not_in_location('M', 3)
        self.assertFalse(letters.is_valid_in_location('M', 3))
        for letter in letters.alphabet:
            if letter != 'M':
                self.assertTrue(letters.is_valid_in_location(letter, 3))

    def test_is_in_location(self):
        letters = Letters(5)
        letters.mark_correct('M', 3)
        self.assertTrue(letters.is_valid_in_location('M', 3))
        for letter in letters.alphabet:
            if letter != 'M':
                self.assertFalse(letters.is_valid_in_location(letter, 3))

    def test_not_in_word(self):
        letters = Letters(5)
        letters.mark_absent('M')
        for location in range(5):
            self.assertFalse(letters.is_valid_in_location('M', 3))

    def test_is_valid(self):
        letters = Letters(5)
        self.assertTrue(letters.is_valid('IRATE'))
        letters.mark_absent('T')
        self.assertFalse(letters.is_valid('IRATE'))

    def test_best_by_score(self):
        letters = Letters(5)
        word_list = load_word_list("wordlist.txt")
        frequencies = [load_letter_frequencies("english_monograms.txt"),
                       load_letter_frequencies("english_bigrams.txt"),
                       load_letter_frequencies("english_trigrams.txt")]
        wp = WordProbability(frequencies)
        letters.mark_absent('T')
        sublist = list(letters.filter_word_list(word_list))
        print(wp.best_words_by_score(sublist, 5))
        print(wp.best_words_by_probability(sublist, 5))