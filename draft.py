import pronouncing
from LilSis import LilSis
from numpy.random import choice

#defines the possible vowel sounds
cmuvowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']
#regexes to find words with exactly this stress pattern
foot_types = ['^01$','^10$']

iambs = pronouncing.search_stresses('^01$')
trochees = pronouncing.search_stresses('^10$')

# create a new lsystem using
#   3 unique symbols ('a','b','c')
#   1 random start string 5 chars long
#   3 random rules of length 2
lsystem = LilSis(symbol_count=3, start_length=5, rule_length=2)

# expand 3 times, creating a template of 40 symbols
template = lsystem.expand(3)

print template

#step 1: pair each symbol in the lsystem
#   to a vowel sound and a foot type (trochee, iamb)
soundmap = {}
for c in lsystem.symbols:
    soundmap[c] = (choice(cmuvowels), choice(foot_types))

print soundmap
#step 2:
