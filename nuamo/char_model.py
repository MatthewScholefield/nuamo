import random
import re
from itertools import product


class CharModel:
    def __init__(self, chain, lookback, real_words=None):
        self.chain = chain
        self.lookback = lookback
        self.real_words = set(real_words or [])

    @classmethod
    def from_vowels(cls):
        vowels = list('aeiouy') + ['ai', 'ae', 'ao', 'au', 'ea', 'ee', 'ei', 'io', 'iu', 'i', 'oa', 'oe', 'oi', 'oo',
                                   'ou', 'ua', 'ue', 'ui']
        fricatives = list('bcdfghijklmnprstvwxz') + ['qu'] + [''.join(i) for i in
                                                              product(list('bcdfgkp'), [''] + list('rlw'))]
        fricatives.remove('fw')
        chain = {**{fr: {**{v: 1 for v in vowels}, '$': 10 ** 10 if len(fr) == 1 else 0} for fr in fricatives},
                 **{v: {fr: 1 for fr in fricatives} for v in vowels}, '^': {fr: 1 for fr in fricatives}}
        del chain['qu']['u']
        return cls({(k,): v for k, v in chain.items()}, 1)

    @classmethod
    def from_text(cls, text, lookback=2):
        chain = {}
        words = re.findall(r'\w+', text)
        for word in words:
            hist = ('^',) * lookback
            for c in word:
                dist = chain.setdefault(hist, {})
                dist[c] = dist.get(c, 0) + 1
                hist = (hist + (c,))[-lookback:]
            dist = chain.setdefault(hist, {})
            dist['$'] = dist.get('$', 0) + 1
        return cls(chain, lookback, words)

    def create_word(self, word_len):
        while True:
            word = self._create_word(word_len)
            if word not in self.real_words and abs(word_len - len(word)) < 4:
                return word

    def _create_word(self, word_len):
        hist = ('^',) * self.lookback
        word = ''
        while True:
            dist = self.chain[hist]
            if '$' in dist:
                dist = dict(dist)
                if len(word) >= word_len:
                    dist['$'] *= sum(dist.values()) * (len(word) - word_len + 2) ** 2
                else:
                    dist.pop('$')
                    if not dist:
                        return word

            choice = random.random() * sum(dist.values())
            it = iter(dist.items())
            char = ''
            while choice >= 0.0:
                char, chance = next(it)
                choice -= chance
            if char == '$':
                break
            word += char
            hist = (hist + (char,))[-self.lookback:]
        return word
