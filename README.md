# Nuamo

*A tool to generate potential project names*

Often times when creating a project name we want to find a
string of characters that's both unique, but intelligible.
Doing this requires a lot of guesswork and internet searches
to see if the name is already taken. This tool automates this
process by using a character level markov chain to generate
strings of characters and scraping Google to identify whether
each character set has already been taken or is too obscure
(too high of entropy like `siufroeb`).

## Installation

Install via pip:

```bash
pip3 install nuamo
```

## Usage

Call via the `nuamo` command like:

```bash
nuamo --word-count 4 --char-lengths 5 --max-results 30000 --min-results 100 --search-delay 2
```
