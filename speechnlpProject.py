# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:58:06 2018

@author: Quentin
"""

"""
    load_CFG_corpus
    Loads the corpus to be learnt
    
    Parameters
    ----------
    path: string. 
        The relative path in which to find the tweet corpus.
    
    Returns
    ----------
    res: list(string). 
        A list of strings corresponding to a list of training samples.
"""
def load_tweet_corpus(path):
    f = open(path, "r")#    
    res = f.read().split("\n")
    f.close()
    return res