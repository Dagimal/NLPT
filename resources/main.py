import fileinput
import random
import re
from nltk.corpus import wordnet as wn
from nltk.corpus import webtext
from nltk import FreqDist

EXTRA_WORD_PROB = 0.2
commonWords = []
for fileid in webtext.fileids():
    commonWords.extend(webtext.words(fileid))
commonWords = FreqDist(commonWords).most_common(500)
commonWords = list(map(lambda x: x[0], commonWords))

def paraphrase(sentence):
    toks = extract_tokens(sentence)
    indices = usable_token_indices(toks)
    for idx in random_subset(indices):
        tok = toks[idx]
        pp = paraphrases(tok[0])
        toks[idx] = (pp[random.randrange(0, len(pp))], tok[1])
    print(join_tokens(toks))

def extract_tokens(sentence):
    separator = u"[\\s\\(\\)\\?;:,\\.\\!\\-’]"
    pattern = "(%s*|^)(.+?)(%s+|$)" % (separator, separator)
    matches = re.findall(pattern, sentence)
    res = []
    for match in matches:
        if match[0] != "": res.append((match[0], False))
        res.append((match[1], True))
        if match[2] != "": res.append((match[2], False))
    return res

def usable_token_indices(toks):
    res = []
    for info in enumerate(toks):
        (i, tok) = info
        if tok[1]:
            if len(paraphrases(tok[0])) > 0:
                res.append(i)
    return res

def paraphrases(word):
    # Avoid common words that double as acronyms, such as
    # "it" or "I".
    if len(word) < 3: return []

    # Replacing common words usually sounds very weird.
    if word in commonWords: return []

    ss = wn.synsets(word)
    res = []
    found = False
    for synset in ss:
        for lemma in synset.lemma_names():
            if lemma == word:
                # Avoid anything but nouns, adjectives, and satellites.
                if synset.pos() not in ["n", "a", "s"]:
                    return []
                found = True
                continue
            if "_" not in lemma and lemma not in res:
                res.append(lemma)

    # Avoid word forms that aren't stemmed.
    if not found: return []

    return res

def random_subset(indices):
    res = []
    if len(indices) == 0:
        return res
    remaining = list(indices)
    while len(res) == 0 or (do_extra_word() and len(remaining) > 0):
        idx = random.randrange(0, len(remaining))
        res.append(remaining[idx])
        del remaining[idx]
    return res

def do_extra_word():
    return random.random() < EXTRA_WORD_PROB

def join_tokens(toks):
    res = ""
    for tok in toks:
        res += tok[0]
    return res

with fileinput.FileInput(bufsize=1) as f:
    while True:
        line = f.readline()
        if line == "": break
        paraphrase(line.rstrip("\r\n"))
