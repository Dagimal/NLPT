import nltk
import random as rand

from nltk.corpus import wordnet as wn

#asks user to input a phrase to change the words and how many random sentences that want to output
phrase = input("Input a phrase:\n")
numberoftimes = input("How many random sentences do you want?\n")

#runs program a certain number of times
for _ in range(int(numberoftimes)):
    rephrased = ''
    #splits sentence in seperate words over spaces
    for word in phrase.split(' '):
        try:
            #picks a random synonym to replace the word with
            synset = wn.synsets(word)
            synonym = synset[0].lemma_names()
            rephrased += str(" " + synonym[rand.randint(0,len(synonym))])

        # if there is a synonym it will be used, otherwise the original word is used
        except IndexError:
            rephrased += " " + word

    #prints final synonym string
    print(rephrased+ '\n')

