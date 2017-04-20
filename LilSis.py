"""
LilSis is a helper module for doing things with L-Systems
"""
from numpy.random import choice

class LilSis:

    def __init__(self, symbols=[], symbol_count=5, start="", start_length=5,rules={}, rule_length=2):
        """Creates a brand-new L-System. Info not provided will be generated based on defaults.

            Max Symbols = 26. Default symbols start at 'a' and continue in alphabetical order, so,
                    LilSis(symbol_count=2, start="abc")
                will prob throw a key error when you try to expand your system.
                Don't do it.

        """

        syms = "abcdefghijklmnopqrstuvwxyz"

        #save or generate the symbol set
        if(len(symbols) == 0):
            self.symbols = list(syms[:symbol_count])
        else:
            self.symbols = symbols

        #save or generate the start phrase
        if len(start) == 0:
            self.start = "".join(choice(self.symbols, start_length))
        else:
            self.start = start

        #save or generate the rules
        if len(rules) == 0:
            self.rules = {}
            for c in self.symbols:
                self.rules[c] = "".join(choice(self.symbols, rule_length))
        else:
            self.rules = rules



    def expand(self, iterations):
        """
        Expand the start string according to the expansion rules provided
        """
        s = self.start
        for i in range(iterations):
            expansion = ""
            for c in list(s):
                expansion += self.rules[c]
            s = expansion
        return s
