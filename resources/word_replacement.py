from nltk import word_tokenize
from nltk.corpus import stopwords
from recipe_scrapers import scrape_me

scraper = scrape_me('https://cookpad.com/uk/recipes/13777213-andhra-chicken-pulao')

stoplist = stopwords.words('english')


def get_synonyms_lexicon(path):
    synonyms_lexicon = {}
    text_entries = [l.strip() for l in open(path).readlines()]
    for e in text_entries:
        e = e.split(' ')
        k = e[0]
        v = e[1:len(e)]
        synonyms_lexicon[k] = v
    return synonyms_lexicon


def synonym_replacement(sentence, synonyms_lexicon):
    keys = synonyms_lexicon.keys()
    words = word_tokenize(sentence)
    n_sentence = sentence
    for w in words:
        if w not in stoplist:
            if w in keys:
                n_sentence = n_sentence.replace(w, synonyms_lexicon[w][0])  # we replace with the first synonym
    return n_sentence


if __name__ == '__main__':
    text = scraper.instructions()
    sentences = text.split('.')
    sentences.remove('')
    #print(sentences)
    synonyms_lexicon = get_synonyms_lexicon('wordnet-synonyms.txt')
    for sentence in sentences:
        new_sentence = synonym_replacement(sentence, synonyms_lexicon)
        #print('%s' % sentence)
        print('%s' % new_sentence)
        #print('\n')
