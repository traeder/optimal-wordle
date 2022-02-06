import math, itertools


class WordProbability:
    def __init__(self, frequencies):
        self.frequencies = frequencies

    def graph_probability(self, graph):
        graph_list = self.frequencies[len(graph)]
        return graph_list[graph]

    def graph_list(self, graph):
        return self.frequencies[len(graph) - 1]

    def conditional_graph_probability(self, graph, given):
        graph_list = self.graph_list(graph)
        given_list = self.graph_list(given)
        my_probability = graph_list[graph]
        base_probability = sum(given_list[g] for g in given_list if g.startswith(given))
        return my_probability / base_probability

    def word_probability(self, word):
        monogram_scores = sum(self.frequencies[0][c] for c in word)
        bigram_scores = sum(self.conditional_graph_probability(word[i:(i+2)], word[i]) for i in range(len(word) - 1))
        trigram_scores = sum(self.conditional_graph_probability(word[i:(i+3)], word[i:(i+3)]) for i in range(len(word) - 2))
        return monogram_scores + bigram_scores + trigram_scores

    def word_rank_score(self, word):
        monograms = self.frequencies[0]
        return sum(math.exp(monograms[c]) for c in set(word))

    def _best_words(self, word_list, func, n):
        scores = {word: func(word) for word in word_list}
        topn = itertools.islice(sorted(scores, key=scores.get, reverse=True), n)
        return list(topn)

    def best_words_by_score(self, word_list, n):
        return self._best_words(word_list, self.word_rank_score, n)

    def best_words_by_probability(self, word_list, n):
        return self._best_words(word_list, self.word_probability, n)


class Letters:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, board_size):
        self.max_val = 2 ** board_size - 1
        self.board_size = board_size
        self.letters = {l: self.max_val for l in self.alphabet}

    def mark_not_present(self, letter):
        self.letters[letter] = 0

    def mark_not_in_location(self, letter, location):
        self.letters[letter] &= (self.max_val - 1 << location)

    def mark_is_in_location(self, letter, location):
        for l in self.letters:
            self.mark_not_in_location(l, location)
        self.letters[letter] = 1 << location

    def is_valid_in_location(self, letter, location):
        return bool(self.letters[letter] & (1 << location))

    def is_valid(self, word):
        if len(word) != self.board_size:
            return False
        return min(self.is_valid_in_location(word[i], i) for i in range(len(word)))

    def filter_word_list(self, word_list):
        return filter(self.is_valid, word_list)


def load_letter_frequencies(file, sep=' '):
    total = 0
    counts = {}
    with open(file) as f:
        for line in f:
            stripped = line.strip()
            word, ct = stripped.split(sep)
            counts[word] = int(ct)
            total += counts[word]

    return {word: math.log(counts[word]) - math.log(total) for word in counts}


def load_word_list(file):
    with open(file) as f:
        ret = [l.strip().upper() for l in f]
    return ret


def get_valid_words(word_list, word_length, known_positions):
    return [w for w in word_list if len(w) == word_length and known_positions.is_valid(w)]
