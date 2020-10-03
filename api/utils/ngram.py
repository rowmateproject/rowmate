import re


def extract_values(d):
    if isinstance(d, dict):
        for v in d.values():
            yield from extract_values(v)
    elif isinstance(d, list):
        for v in d:
            yield from extract_values(v)
    else:
        yield d


def make_ngrams(object, min=1):
    words = [w.split(' ') for w in extract_values(object)]
    wordlist = [re.sub(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', '', x)
                for x in extract_values(words)]
    keyword = []

    for word in list(set(sorted(wordlist))):
        sizes = range(min, max(len(word), min) + 1)
        [[keyword.append(word[i:i + x])
          for i in range(0, max(0, len(word) - x) + 1)] for x in sizes]

    return ' '.join(list(set(sorted(keyword)))).strip()
