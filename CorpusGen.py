"""
This script takes the CMU Pronouncing Dictionary and puts out a json file of iambs and trochees sorted by vowel sound.
"""
import json

# file paths
dict_path = 'cmudict-0.7b'
lexicon_path = 'lexicon.json'

cmuvowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']


def get_vowels(phonemes):
    vs = []
    for p in phonemes:
        if(p.startswith(tuple(cmuvowels))):
            vs.append(p)
    return vs

#lexicon object
words = {}
words["total"] = 0
words["frequency"] = {}

#create empty lists of words for each foot + vowel sound
#start frequency counts for each foot + vowel combo
for v in cmuvowels:
    words["I_" + v] = []
    words["frequency"]["I_" + v] = 0
    words["T_" + v] = []
    words["frequency"]["T_" + v] = 0

def make_lexicon():
    iamb_count = 0
    trochee_count = 0
    with open(dict_path, 'r') as in_f:
        for line in in_f:
            tokens = line.split()
            word = tokens[0]        #first token is the regular word
            phonemes = tokens[1:]   #the rest of them are phonemes
            vowels = get_vowels(phonemes)
            if len(vowels) == 2:
                if vowels[0].endswith('0'):
                    #iamb: the first syllable is unstressed
                    words["I_" + vowels[1][:2]].append(word)
                    words["frequency"]["I_" + vowels[1][:2]] += 1
                    words["total"] += 1
                elif vowels[1].endswith('0'):
                    #the second syllable is unstressed
                    words["T_" + vowels[0][:2]].append(word)
                    words["frequency"]["T_" + vowels[1][:2]] += 1
                    words["total"] += 1

        with open(lexicon_path, 'w') as outfile:
            json.dump(words, outfile)




make_lexicon()
