import pronouncing
from LilSis import LilSis
from numpy.random import choice, randint
from textwrap import wrap

# the idea is to take a string of characters generated by an l-system and then convert them twice:

# in the first conversion, we associate symbols with vowel sounds and stress patterns.
# let's list the possible vowel sounds:

cmuvowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']

# now a list of stress patterns. Each symbol maps to two syllables with a single stressed vowel.

foot_types = ['01','10']

# create a helper function to associate a list of symbols with random sounds from these lists. it returns a pair of dictionary objects
def map_symbols_to_random_sounds(symbols, vowels, feet):
    vowelmap, footmap = {},{}
    for s in symbols:
        vowelmap[s] = choice(vowels)
        footmap[s] = choice(feet)
    return vowelmap, footmap


# then we search for a sequence of words that can realize those patterns.

# here's a function that takes a stress pattern and returns a list of words that match the most syllables possible. If the full pattern doesn't fit, it gets desperate and starts looking for shorter matching stress patterns.
# eventually it returns the words it found and the # of syllables matched
# this was just a dry run of the eventual word_search function
def stress_search(stress_pattern):
    regex = '^' + stress_pattern.replace('1', '[12]') + '$'
    pat_len = len(stress_pattern)
    results = []
    while(not results):
        results = pronouncing.search_stresses(regex)
        pat_len -= 1
        regex = '^' + stress_pattern[:pat_len].replace('1','[12]') + '$'
    return results, pat_len + 1

#pass in a list of syllable regexes and it'll find the set of the longest possible words that fit. We exploit the fact that every syllable is paired with a numeric stress value in order to ignore consonants but catch every vowel.
# if it doesn't find the longest possible match, it gets desperate and starts cutting down the pattern till it finds something.
# there are plenty of single syllable words so it always does eventualy,
# especially because we're not picky about the sound of unstressed syllables.
def word_search(syllable_list):

    regex = '^\D*' + '\D*'.join(syllable_list) + '\D*$'

    pat_len = len(syllable_list)

    results = []
    while(not results):
        #print "WORD SEARCH IS ABOUT TO LOOK FOR THIS PATTERN: "
        #print regex
        #print "IT'S %d SYLLABLES LONG." % pat_len
        results = pronouncing.search(regex)
        pat_len -= 1
        regex = '^\D*' + '\D*'.join(syllable_list[:pat_len]) + '\D*$'
    return results, pat_len + 1


#takes a template and a sound/stress map and writes a line.
def create_line(template, sounds, stresses):

    #build a list of syllable regexes sought
    syllables = []
    for c in template:
        #go through each digit of the stress pattern
        for n in list(stresses[c]):
            #add a sound to stressed syllables and relax the stress requirements
            syl_regex = n.replace('1', sounds[c]+'[12]')
            syllables.append(syl_regex)

    wordlist = []
    unprocessed = syllables

    while(unprocessed):
        search_string = unprocessed[:randint(1,min(len(unprocessed)+1,4))]
        #print "LOOKING FOR WORDS THAT FIT THIS PATTERN: " + " ".join(search_string)
        possible_words, syllables_used = word_search(search_string)
        #print "FOUND %d WORDS THAT ARE %d syllables long" % (len(possible_words), syllables_used)
        the_exact_right_word = choice(possible_words)
        #print "I'M GOING TO USE " + the_exact_right_word
        wordlist.append(the_exact_right_word)
        unprocessed = unprocessed[syllables_used:]

    return " ".join(wordlist)

# create a new lsystem using
#   3 unique symbols ('a','b','c')
#   1 random start string 5 chars long
#   3 random rules of length 2
lsystem = LilSis(symbol_count=5, start_length=5, rule_length=2)

# expand 3 times, creating a template of 40 symbols
template = lsystem.expand(3)

line_patterns = [lsystem.start] + wrap(template, 5)

#step 1: pair each symbol in the lsystem
#   to a vowel sound and a foot type (trochee, iamb)
soundmap, stressmap = map_symbols_to_random_sounds(lsystem.symbols, cmuvowels, foot_types)

print "Vowel Sounds:"
print soundmap
print "Stresses:"
print stressmap
print "The Template:"
for l in line_patterns:
    print l

print "\nAnd now, the poem:"
for l in line_patterns:
    print create_line(l, soundmap, stressmap)

print "\nAnd here's a 9 line poem using only the title pattern:\n"
print create_line(lsystem.start, soundmap, stressmap)
print "\n"
print create_line(lsystem.start, soundmap, stressmap)
print create_line(lsystem.start, soundmap, stressmap)
print create_line(lsystem.start, soundmap, stressmap)
print create_line(lsystem.start, soundmap, stressmap)
print "\n"
print create_line(lsystem.start, soundmap, stressmap)
print create_line(lsystem.start, soundmap, stressmap)
print create_line(lsystem.start, soundmap, stressmap)
print create_line(lsystem.start, soundmap, stressmap)
