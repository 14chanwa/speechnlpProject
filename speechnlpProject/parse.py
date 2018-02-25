# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:58:06 2018

@author: Quentin
"""


from speechnlpProject.grammar import *
import numpy as np


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
def _recursive_parse_transition_level(test_s, to_lower_case=False):
    
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
            res += _recursive_parse_transition_level(_test_s, to_lower_case)
        
        return res
        
    else:
        # Get terminal symbol
        sym = test_s.split(' ', 2)[1]
        
        if to_lower_case:
            sym = sym.lower()

        syms_next_level.append(GSymbol(sym, GSymbol.TERMINAL))
        
        res = [GTransition(nts, syms_next_level)]
        
        return res


def remove_nt_to_nt(l_gtrans):
    
    l_gtrans2 = list()
    map_nt_to_nt = {}
    
    # For each GTransition
    for gtrans in l_gtrans:
        new_res_symb = gtrans.res_symb()
        while len(new_res_symb) == 1 and \
            new_res_symb[0].stype() == GSymbol.NON_TERMINAL:
            # Dig until find a terminal or more than 2 non-terminals
            for gtrans2 in l_gtrans:
                if gtrans2.symb() == new_res_symb[0]:
                    if gtrans2.symb() not in map_nt_to_nt.keys():
                        map_nt_to_nt[gtrans2.symb()] = set()
                    map_nt_to_nt[gtrans2.symb()].add(gtrans.symb())
                    new_res_symb = gtrans2.res_symb()
                    break
        l_gtrans2.append(GTransition(gtrans.symb(), new_res_symb))
    
    # Append all missing GTransitions
    # Initial length of the list
    n_init = len(l_gtrans2)
    for i in range(n_init):
        symbol_to_map = l_gtrans2[i].symb()
        if symbol_to_map in map_nt_to_nt.keys():
            for gsymb in map_nt_to_nt[symbol_to_map]:
                l_gtrans2.append(GTransition(gsymb, l_gtrans2[i].res_symb()))
    #~ print(map_nt_to_nt)
    
    return l_gtrans2


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
def parse_transitions(test_s, to_lower_case=False):
    
    # Remove unused parenthesis
    while test_s.lstrip()[0] == "(":
        test_s = parse_parenthesis_blocks(test_s)[0]
    
    parsed_transitions = _recursive_parse_transition_level(test_s, to_lower_case)
    parsed_transitions = remove_nt_to_nt(parsed_transitions)
    
    return Counter(parsed_transitions)


class CYK_Parser:
    
    
    def __init__(self, pcfg, root_symbol, verbose=False):
        self._pcfg = pcfg
        self._root_symbol = root_symbol
        self.verbose = verbose
    
    
    def _recursive_string_construction(self, cyk_table, i, j, gsymb):
        
        # Get transition
        gtrans = cyk_table[i][j][gsymb][0]
        
        # If transition maps to a terminal, return the terminal
        if gtrans.res_symb()[0].stype() == GSymbol.TERMINAL:
            return str(gsymb) + " " + gtrans.res_symb()[0].ssymb()
        
        # else, recursively get the transitions
        return str(gsymb) + " (" + \
            self._recursive_string_construction(cyk_table, \
                cyk_table[i][j][gsymb][2], \
                cyk_table[i][j][gsymb][3], \
                cyk_table[i][j][gsymb][0].res_symb()[0]) + ") (" + \
            self._recursive_string_construction(cyk_table, \
                cyk_table[i][j][gsymb][4], \
                cyk_table[i][j][gsymb][5], \
                cyk_table[i][j][gsymb][0].res_symb()[1]) + ")"
    
    
    def parse(self, test_s):
        
        # Parse spaces in string
        input_string = test_s.split(' ')
        
        n = len(input_string)
        
        # Check if words in lexicon
        for w in input_string:
            if w not in self._pcfg.lexicon().keys():
                #~ raise Exception("Unrecognized word:" + w)
                print("Unrecognized word: " + w)
                return None
        
        # Perform CYK
        # Build a table.
        cyk_table = []
        
        # First level: non-terminals corresponding to words
        # The first row of cyk_table will be:
        # [ {non-terminal: (GTransition, logvalue)}, ...
        #       {non-terminal: (GTransition, logvalue)}...] (length n)
        # where logvalue is the log-probability of this non-terminal 
        # leading to this terminal.
        
        cyk_table.append([])
        current_row = cyk_table[0]
        
        for i in range(n):
            current_row.append({})
            current_cell = current_row[i]
            
            # Get terminal symbol
            ts = input_string[i]
            
            # Add all {non-terminal: probability}
            # Get non-terminals that lead to this terminal
            for nts in self._pcfg.lexicon()[ts]:
                current_max_log_proba = -np.inf
                for trans, val in self._pcfg.root_to_trans(nts).items():
                    if np.log(val) > current_max_log_proba and trans.res_symb()[0].ssymb() == ts:
                        current_cell[nts] = (trans, np.log(val))
                        current_max_log_proba = np.log(val)
        
        
        for lev in range(1, n):
            # Level lev: on this row, all combinations:
            # [{GSymbol: (GTransition, logvalue, i, j, i', j'))}, \
            #        {GSymbol: (GTransition, logvalue, i, j, i', j'))}...]
            # such that on the position j the GSymbol can be constructed by 
            # combining a subword at position (i, j) and (i', j') given by
            # the transition GTransition with max log probability logvalue.
            cyk_table.append([])
            current_row = cyk_table[lev]
            for k in range(n-lev):
                current_row.append({})
                current_cell = current_row[k]
                # On k column, get the possible combinations to get a
                # suitable substring
                # Iterate over combinations
                for i in range(lev):
                    # Get all symbols on cell (i, k) and cell (lev-i-1, k+1+i)
                    candidate_symbols_1 = cyk_table[i][k].keys()
                    candidate_symbols_2 = cyk_table[lev-i-1][k+1+i].keys()
                    if self.verbose:
                        print("cell1:", (i, k))
                        print("cell2:", (lev-i-1, k+1+i))
                    for c1 in candidate_symbols_1:
                        for c2 in candidate_symbols_2:
                            if self.verbose:
                                print("for candidates", c1, c2, "found:", self._pcfg.res_to_trans((c1, c2)))
                            weight = cyk_table[i][k][c1][1] + cyk_table[lev-i-1][k+1+i][c2][1]
                            # Look for transitions
                            for trans, value in self._pcfg.res_to_trans((c1, c2)).items():
                                # Add combination or replace if probability is greater
                                if trans.symb() not in current_cell.keys() or weight + np.log(value) > current_cell[trans.symb()][1]:
                                    current_cell[trans.symb()] = (trans, weight + np.log(value), i, k, lev-i-1, k+1+i)
                if self.verbose:            
                    print("\n")
        
        if self.verbose:
            print("Unweighted CYK table:")
            for lev in range(n-1, -1, -1):
                print([sorted(list(gsymb.keys())) for gsymb in cyk_table[lev]])
        if self._root_symbol in cyk_table[n-1][0].keys():
            if self.verbose:
                print("Found " + str(self._root_symbol) + " in top level with logp=" + str(cyk_table[n-1][0][self._root_symbol][1]))
            return "(" + self._recursive_string_construction(cyk_table, n-1, 0, self._root_symbol) + ")"
        
        return None
        
