# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:58:06 2018

@author: Quentin
"""


from speechnlpProject.grammar import *
from speechnlpProject.parse import *
import sys


# USAGE:
# python test_main.py "Amélioration de la sécurité\nGutenberg"


def load_CFG_corpus(path):
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
    f = open(path, "r")#    
    res = f.read().split("\n")
    f.close()
    return res


def split_train_dev_test(cfg_corpus):
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
    n = len(cfg_corpus)
    n_train = int(n * 0.8)
    n_dev = int((n-n_train) // 2)
    n_test = n - n_train - n_dev
    
    print("n_train=", n_train, "n_dev=", n_dev, "n_test=", n_test)
    
    cfg_corpus_train = cfg_corpus[:n_train]
    cfg_corpus_dev = cfg_corpus[n_train:n_train+n_dev]
    cfg_corpus_test = cfg_corpus[n_train+n_dev:]
    
    return cfg_corpus_train, cfg_corpus_dev, cfg_corpus_test


cfg_corpus = load_CFG_corpus("sequoia-corpus+fct.mrg_strict")
cfg_corpus_train, cfg_corpus_dev, cfg_corpus_test = split_train_dev_test(cfg_corpus)


# Train on training corpus
b = PCFG(cfg_corpus_train, chomsky_normalize=True)

print(len(b.nt_symbs()), "non-terminals")
print(len(b.lexicon()), "words")

parser = CYK_Parser(b, GSymbol("SENT", GSymbol.NON_TERMINAL), verbose=False)


# Get input test corpus (tokenized!)
#~ print(sys.argv[1])

if len(sys.argv) < 2:
    raise Exception("Empty input!")

input_test_corpus = sys.argv[1].split("\n")
input_test_corpus_2 = []
for i in range(len(input_test_corpus)):
    input_test_corpus_2 += input_test_corpus[i].split("\\n")


for i in range(0, len(input_test_corpus_2)):
    parsed_sent = input_test_corpus_2[i]
    print(">>> Parsing: " + parsed_sent)
    print(parser.parse(parsed_sent.lower()))
