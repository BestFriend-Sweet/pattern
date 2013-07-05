#### PATTERN | IT ##################################################################################
# -*- coding: utf-8 -*-
# Copyright (c) 2013 University of Antwerp, Belgium
# Copyright (c) 2013 St. Lucas University College of Art & Design, Antwerp.
# Author: Tom De Smedt <tom@organisms.be>, Fabio Marfia <marfia@elet.polimi.it>
# License: BSD (see LICENSE.txt for details).

####################################################################################################

import os
import sys

try:
    MODULE = os.path.dirname(os.path.abspath(__file__))
except:
    MODULE = ""

sys.path.insert(0, os.path.join(MODULE, "..", "..", "..", ".."))

# Import parser base classes.
from pattern.text import (
    Lexicon, Spelling, Parser as _Parser, ngrams, pprint, commandline,
    PUNCTUATION
)
# Import parse tree base classes.
from pattern.text.tree import (
    Tree, Text, Sentence, Slice, Chunk, PNPChunk, Chink, Word, table,
    SLASH, WORD, POS, CHUNK, PNP, REL, ANCHOR, LEMMA, AND, OR
)
# Import sentiment analysis base classes.
from pattern.text import (
    Sentiment, NOUN, VERB, ADJECTIVE, ADVERB
)
# Import verb tenses.
from pattern.text import (
    INFINITIVE, PRESENT, PAST, FUTURE, CONDITIONAL,
    FIRST, SECOND, THIRD,
    SINGULAR, PLURAL, SG, PL,
    INDICATIVE, IMPERATIVE, SUBJUNCTIVE,
    IMPERFECTIVE, PERFECTIVE, PROGRESSIVE,
    IMPERFECT, PRETERITE,
    PARTICIPLE, GERUND
)
# Import inflection functions.
from pattern.text.it.inflect import (
    article, referenced, DEFINITE, INDEFINITE,
    pluralize, singularize, NOUN, VERB, ADJECTIVE,
    verbs, conjugate, lemma, lexeme, tenses,
    predicative, attributive,
    gender, MASCULINE, MALE, FEMININE, FEMALE, NEUTER, NEUTRAL, PLURAL, M, F, N, PL
)
# Import all submodules.
from pattern.text.it import inflect

sys.path.pop(0)

#--- PARSER ----------------------------------------------------------------------------------------

ABBREVIATIONS = [
    "a.C.", "all.", "apr.", "art.", "artt.", "b.c.", "c.a.", "cfr.", "c.d.", 
    "c.m.", "C.V.", "d.C.", "Dott.", "ecc.", "egr.", "e.v.", "fam.", "giu.", 
    "Ing.", "L.", "n.", "op.", "orch.", "p.es.", "Prof.", "prof.", "ql.co.", 
    "secc.", "sig.", "s.l.m.", "s.r.l.", "Spett.", "S.P.Q.C.", "v.c."
]

replacements = (
    "a", "co", "all", "anch", "nient", "cinquant", 
    "b", "de", "dev", "bell", "quell", "diciott",
    "c", "gl", "don", "cent", "quest", "occupo",
    "d", "po", "dov", "dall", "trent", "sessant",
    "l", "un", "nel", "dell", "tropp",
    "m",              "king",
    "n",              "nell",
    "r",              "sant",
    "s",              "sott",
                      "sull",
                      "tant",
                      "tutt",
                      "vent")

replacements += tuple(k.capitalize() for k in replacements)
replacements  = dict((k+"'", k+"' ") for k in replacements)

def find_lemmata(tokens):
    """ Annotates the tokens with lemmata for plural nouns and conjugated verbs,
        where each token is a [word, part-of-speech] list.
    """
    for token in tokens:
        word, pos, lemma = token[0], token[1], token[0]
        if pos.startswith(("DT",)):
            lemma = singularize(word, pos="DT")
        if pos.startswith("JJ"):
            lemma = predicative(word)  
        if pos == "NNS":
            lemma = singularize(word)
        if pos.startswith(("VB", "MD")):
            lemma = conjugate(word, INFINITIVE) or word
        token.append(lemma.lower())
    return tokens

class Parser(_Parser):
    
    def find_tokens(self, tokens, **kwargs):
        kwargs.setdefault("abbreviations", ABBREVIATIONS)
        kwargs.setdefault("replace", replacements)
        return _Parser.find_tokens(self, tokens, **kwargs)

    def find_lemmata(self, tokens, **kwargs):
        return find_lemmata(tokens)

lexicon = Lexicon(
        path = os.path.join(MODULE, "it-lexicon.txt"), 
  morphology = os.path.join(MODULE, "it-morphology.txt"), 
     context = os.path.join(MODULE, "it-context.txt"),
    language = "it"
)

parser = Parser(
     lexicon = lexicon,
     default = ("NN", "NNP", "CD"),
    language = "it"
)

def tokenize(s, *args, **kwargs):
    """ Returns a list of sentences, where punctuation marks have been split from words.
    """
    return parser.find_tokens(s, *args, **kwargs)

def parse(s, *args, **kwargs):
    """ Returns a tagged Unicode string.
    """
    return parser.parse(s, *args, **kwargs)

def parsetree(s, *args, **kwargs):
    """ Returns a parsed Text from the given string.
    """
    return Text(parse(s, *args, **kwargs))

def split(s, token=[WORD, POS, CHUNK, PNP]):
    """ Returns a parsed Text from the given parsed string.
    """
    return Text(s, token)
    
def tag(s, tokenize=True, encoding="utf-8"):
    """ Returns a list of (token, tag)-tuples from the given string.
    """
    tags = []
    for sentence in parse(s, tokenize, True, False, False, False, encoding).split():
        for token in sentence:
            tags.append((token[0], token[1]))
    return tags

#---------------------------------------------------------------------------------------------------
# python -m pattern.it xml -s "Il gatto nero faceva le fusa." -OTCL

if __name__ == "__main__":
    commandline(parse)