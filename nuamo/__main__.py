#!/usr/bin/env python3

import random
from argparse import ArgumentParser

from nuamo.char_model import CharModel
from nuamo.google_searcher import GoogleSearcher


def parse_range(s):
    if ',' in s:
        return sum([parse_range(i) for i in s.split(',')], [])
    if '-' in s:
        a, b = map(int, s.split('-'))
        return list(range(a, b + 1))
    return [int(s)]


def load_model(args):
    if args.train_text:
        with open(args.train_text) as f:
            text = f.read()
        return CharModel.from_text(text)
    else:
        return CharModel.from_vowels()


def generate_words(model, searcher, args):
    while True:
        test_word = model.create_word(random.choice(args.char_lengths))
        if args.no_search:
            yield test_word, None
        else:
            results = searcher.get_num_results(test_word)
            is_valid = args.min_results <= results <= args.max_results
            if is_valid:
                yield test_word, results
            if not args.quiet:
                print('Option:' if is_valid else 'Failed:', test_word, '-', results)


def main():
    parser = ArgumentParser(description='Tool to generate potential project names')
    parser.add_argument('-t', '--train-text', help='Text file to generate character model from')
    parser.add_argument('-l', '--lookback', default=2, type=int, help='Lookback to use in markov chain from text model')
    parser.add_argument('-w', '--word-count', type=int, default=4, help='Number of words to generate')
    parser.add_argument('-c', '--char-lengths', type=parse_range, default='5', help='Lengths of characters')
    parser.add_argument('-m', '--max-results', type=int, default=30000, help='Max search results for a valid name')
    parser.add_argument('-n', '--min-results', type=int, default=100, help='Min search results for a valid name')
    parser.add_argument('-d', '--search-delay', type=float, default=2.0, help='Delay between searches to prevent captcha')
    parser.add_argument('-q', '--quiet', action='store_true', help='Only output project name info')
    parser.add_argument('--no-search', action='store_true', help='Skip calculating search results')
    args = parser.parse_args()

    model = load_model(args)
    searcher = GoogleSearcher(args.search_delay)

    words = [word for word, _ in zip(generate_words(model, searcher, args), range(args.word_count))]

    if not args.quiet:
        print()
        print('=== Project Names ===')

    for word, results in words:
        if results is None:
            print(word)
        else:
            print(word, '-', results)


if __name__ == '__main__':
    main()
