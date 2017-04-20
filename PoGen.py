""" NaPoGenMo Entry
Use an l-system to create a prosodic/vocalic map of the poem-to-be. Each symbol represents a two-syllable word and identifies both its stress pattern and the vowel sound of its stressed syllable. (The corpus is limited to iambs and trochees.)"""

"""
The start phrase consists of five symbols and will eventually become the new poem's title. The symbol expansion rules are each two symbols long, so that every line of five symbols expands into a pentametric couplet.
"""

import json
from LilSis import LilSis
from numpy import split
from numpy import array
from numpy.random import choice
from textwrap import wrap

alphabet = "abcdefghijklmnopqrstuvwxyz"

unique_symbols = 3
symbols = list(alphabet[:unique_symbols])
rule_length = 2
line_length = 5
iterations = 4

def write_poem_from_template(template, lexicon):
    #Step 1: Find the relative frequency of each vowel sound/foot combo
    foot_types, prob = [], []
    total = float(lexicon["total"])
    for k, v in lexicon["frequency"].items():
        foot_types.append(k)
        prob.append(v/total)

    #Step 2: Pick which types of feet to use
    feet = choice(foot_types, unique_symbols, False, prob)
    print feet

    #Step 3: Build a symbol to foot translation table
    sym_table = dict(zip(symbols, feet))
    print sym_table

    #Step 4: Translate the template lines into words
    expanded_lines = []
    for line in template:
        wl = []
        for c in line:
            #translate c into a foot type & pick a random word that matches
            wl.append(choice(lexicon[sym_table[c]]))
        expanded_lines.append(" ".join(wl))

    #Step 5: Break into stanzas and modify the capitalization
    title = expanded_lines[0].title()

    unjoined_stanzas = split(array(expanded_lines[1:]), 2 ** (iterations - 2))
    stanzas = []

    for st in unjoined_stanzas:
        stanzas.append(",\n".join(st).capitalize()+".")

    poem = '\n\n'.join([title] + stanzas)

    return poem

lsystem = LilSis()
poem_template = lsystem.expand(iterations)
print poem_template
with open("lexicon.json", 'r') as f:
    #Step 1: Load lexicon
    lexicon = json.load(f)

    poem = write_poem_from_template(poem_template, lexicon)
    print poem
