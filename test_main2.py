# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:58:06 2018

@author: Quentin
"""


from speechnlpProject.grammar import *
from speechnlpProject.parse import *


"""
    load_CFG_corpus
    Loads the corpus to be learnt
    
    Parameters
    ----------
    path: string. 
        The relative path in which to find the corpus.
    
    Returns
    ----------
    res: list(string). 
        A list of strings corresponding to a list of samples.
"""
def load_CFG_corpus(path):
    f = open(path, "r")#    
    res = f.read().split("\n")
    f.close()
    return res


"""
    split_train_dev_test
    Splits the corpus in 3 parts (80, 10, 10 %).
    
    Parameters
    ----------
    cfg_corpus: list(string). 
    
    Returns
    ----------
    cfg_corpus_train: list(string). 
    cfg_corpus_dev: list(string). 
    cfg_corpus_test: list(string). 
"""
def split_train_dev_test(cfg_corpus):
    n = len(cfg_corpus)
    n_train = int(n * 0.8)
    n_dev = int((n-n_train) // 2)
    n_test = n - n_train - n_dev
    
    print("n_train=", n_train, "n_dev=", n_dev, "n_test=", n_test)
    
    cfg_corpus_train = cfg_corpus[:n_train]
    cfg_corpus_dev = cfg_corpus[n_train:n_train+n_dev]
    cfg_corpus_test = cfg_corpus[n_train+n_dev:]
    
    return cfg_corpus_train, cfg_corpus_dev, cfg_corpus_test


#~ import re

cfg_corpus = load_CFG_corpus("sequoia-corpus+fct.mrg_strict")

#~ for i in range(10):
    #~ print(cfg_corpus[i])

cfg_corpus_train, cfg_corpus_dev, cfg_corpus_test = split_train_dev_test(cfg_corpus)


test_s = "( (SENT (AP (PREF Cardio-) (ADJ pulmonaire))))"#cfg_corpus_train[11]

print(test_s)

#~ print(GSymbol("S", 0) == GSymbol("S", 0))
#~ print(GSymbol("S", 0) == GSymbol("S", 1))
#~ print(GSymbol("T", 0) == GSymbol("S", 0))

#~ s = {}
#~ s[GSymbol("S", 0)] = 0
#~ s[GSymbol("S", 0)] = 1
#~ print(s)

parsed_transitions = parse_transitions(test_s, to_lower_case=True)

print(parsed_transitions)


#~ for i in range(len(cfg_corpus_train)):
    #~ parsed_transitions += parse_transitions(cfg_corpus_train[i], to_lower_case=True)

#~ for elt in parsed_transitions.elements():
    #~ print(elt)

#~ b = PCFG(parsed_transitions, chomsky_normalize=True)
#~ print(b)

#~ print(b.trans(GSymbol("SENT", 0)))

#~ print(len(b.nt_symbs()), "non-terminals")
#~ print(len(b.lexicon()), "words")


#~ print(b._cfg_inversemap)

#~ parser = CYK_Parser(b, GSymbol("SENT", GSymbol.NON_TERMINAL))

#~ print(parser.parse(("Pourquoi ce thème ?").lower()))


