# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:58:06 2018

@author: Quentin
"""

from speechnlpProject.grammar import *


"""
    parse_parenthesis_blocks
    Parse the first level of parenthesis blocks in the provided string.
    E.g. on
        "((1, a) (2, b))"
    will return:
        ["(1, a) (2, b)"]
    but on
        "(1, a) (2, b)"
    will return:
        ["(1, a)", "(2, b)"]
    
    Parameters
    ----------
    test_s: string. 
        The string to be parsed.
    
    Returns
    ----------
    parsed: list(string). 
        A list of parsed parenthesis blocks.
"""
def parse_parenthesis_blocks(test_s):
    parsed = []
    n_opened = 0
    i_opened = 0
    
    for cursor in range(len(test_s)):
        if test_s[cursor] == "(":
            if n_opened == 0:
                i_opened = cursor
            n_opened += 1
            
        elif test_s[cursor] == ")":
            n_opened -= 1
            if n_opened == 0:
                #print(i_opened+1, cursor)
                parsed.append(test_s[i_opened+1:cursor])
    
    return parsed


"""
    parse_transition_level
    Parse the next level of transitions.
    E.g. on
        "((1, a) (2, b))"
    will return:
        ["(1, a) (2, b)"]
    but on
        "(1, a) (2, b)"
    will return:
        ["(1, a)", "(2, b)"]
    Suppose no terminal is left alone without any non-terminal wrapping,
    i.e. a terminal will always look like: (TER terminal).
    
    Parameters
    ----------
    test_s: string. 
        The formatted string to be parsed. E.g.:
            "NP-SUJ (DET Cette) (NC exposition)"
    
    Returns
    ----------
    nts: GTransition.
        The current transition.
    s_next_level: list(string).
        A list of strings corresponding to the next levels, for further
        investigation.
"""
def parse_transition_level(test_s):
    
    # Suppose the first token is the non-terminal symbol
    nts = test_s.split(' ', 1)[0]
    nts = nts.split('-', 1)[0]
    nts = GSymbol(nts, GSymbol.NON_TERMINAL)
    
    # Parse parenthesis blocks
    syms_next_level = []
    s_next_level = parse_parenthesis_blocks(test_s)
    
    if len(s_next_level) > 0:
        # Get non-terminal symbols
        next_nts = []
        for s_next in s_next_level:
            sym = s_next.split(' ', 1)[0]
            sym = sym.split('-', 1)[0]
            syms_next_level.append(GSymbol(sym, GSymbol.NON_TERMINAL))
    else:
        # Get terminal symbol
        sym = test_s.split(' ', 2)[1]
        syms_next_level.append(GSymbol(sym, GSymbol.TERMINAL))
    
    ntr = GTransition(nts, syms_next_level)
    
    return ntr, s_next_level


"""
    _recursive_parse_transition_level
    Parse the next level of transitions recursively.
    E.g. on
        "((1, a) (2, b))"
    will return:
        ["(1, a) (2, b)"]
    but on
        "(1, a) (2, b)"
    will return:
        ["(1, a)", "(2, b)"]
    Suppose no terminal is left alone without any non-terminal wrapping,
    i.e. a terminal will always look like: (TER terminal).
    RECURSIVE VERSION
    
    Parameters
    ----------
    test_s: string. 
        The formatted string to be parsed. E.g.:
            "NP-SUJ (DET Cette) (NC exposition)"
    
    Returns
    ----------
    nts: list(GTransition).
        List of transitions in test_s (with multiplicities).
"""
def _recursive_parse_transition_level(test_s):
    
    # Suppose the first token is the non-terminal symbol
    nts = test_s.split(' ', 1)[0]
    nts = nts.split('-', 1)[0]
    nts = GSymbol(nts, GSymbol.NON_TERMINAL)
    
    # Parse parenthesis blocks
    syms_next_level = []
    s_next_level = parse_parenthesis_blocks(test_s)
    
    if len(s_next_level) > 0:
        # Get non-terminal symbols
        next_nts = []
        for s_next in s_next_level:
            sym = s_next.split(' ', 1)[0]
            sym = sym.split('-', 1)[0]
            syms_next_level.append(GSymbol(sym, GSymbol.NON_TERMINAL))
        
        res = [GTransition(nts, syms_next_level)]
        for _test_s in s_next_level:
            res += _recursive_parse_transition_level(_test_s)
        
        return res
        
    else:
        # Get terminal symbol
        sym = test_s.split(' ', 2)[1]
        syms_next_level.append(GSymbol(sym, GSymbol.TERMINAL))
        
        res = [GTransition(nts, syms_next_level)]
        
        return res


"""
    parse_transitions
    Parse and count transitions in the provided string.

    Parameters
    ----------
    test_s: string. 
        The string to be parsed. E.g.:
            "(NP-SUJ (DET Cette) (NC exposition))"
        or:
            "NP-SUJ (DET Cette) (NC exposition)"

    Returns
    ----------
    nts: Counter({GTransition : n}).
        Counter of different transitions.
"""
def parse_transitions(test_s):
    
    # Remove unused parenthesis
    while test_s.lstrip()[0] == "(":
        test_s = parse_parenthesis_blocks(test_s)[0]
    
    return Counter(_recursive_parse_transition_level(test_s))
