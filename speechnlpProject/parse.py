# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:58:06 2018

@author: Quentin
"""


from speechnlpProject.grammar import *
import numpy as np


"""
    edit_distance
    Computes the Levenshtein distance between 2 given strings using the
    Wagner–Fischer algorithm.
    The Levenshtein distance takes into account insert, delete, replace 
    operations.
    
    Parameters
    ----------
    s1: string. First string.
    s2: string. Second string.
    
    Returns
    ----------
    res: int. The Levenshtein distance between s1 and s2.
    """
def edit_distance(s1, s2):
    # Note that compared to the psuedo code given in the slides:
    # - arrays indices in python begin at 0
    # - m is in fact of shape (len(s1)+1, len(s2)+1)
    # - strings indices in python begin at 0
    # We make the suitable index changes
    m = np.zeros((len(s1)+1, len(s2)+1), dtype=int)
    m[:, 0] = np.arange(0, len(s1)+1)
    m[0, :] = np.arange(0, len(s2)+1)
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                m[i, j] = np.min([m[i-1, j]+1, m[i, j-1]+1, m[i-1, j-1]])
                #m[i, j] = m[i-1, j-1]
            else:
                m[i, j] = np.min([m[i-1, j]+1, m[i, j-1]+1, \
                                        m[i-1, j-1]+1])
    return m[len(s1), len(s2)]


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
            return str(gsymb) + " " + cyk_table[i][j][gsymb][2]
        
        # If the current symbol is a X***, do not print it
        if len(gsymb.ssymb()) > 1 and gsymb.ssymb()[0] == "X" and gsymb.ssymb()[1].isdigit():
            return self._recursive_string_construction(cyk_table, \
                    cyk_table[i][j][gsymb][2], \
                    cyk_table[i][j][gsymb][3], \
                    cyk_table[i][j][gsymb][0].res_symb()[0]) + ") (" + \
                self._recursive_string_construction(cyk_table, \
                    cyk_table[i][j][gsymb][4], \
                    cyk_table[i][j][gsymb][5], \
                    cyk_table[i][j][gsymb][0].res_symb()[1])
        
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
        
        i = 0
        j = 0
        while i < n:
            
            # Get terminal symbol
            ts_init = input_string[j]
            
            skip_word = False
            
            # If the word is not recognize, take the word with shorter
            # edit distance <= 2 with highest probability
            if ts_init in self._pcfg.lexicon().keys():
                ts = ts_init
            else:
                #~ raise Exception("Unrecognized word:" + w)
                print("Unrecognized word: " + ts_init + ". Looking for replacement...")
                
                # Get a word in lexicon with edit distance < 3
                max_edit_distance = 3
                replacement_string_map = []
                for z in range(max_edit_distance):
                    replacement_string_map.append({})
                for lexw in self._pcfg.lexicon().keys():
                    current_edit_distance = edit_distance(ts_init, lexw)
                    if current_edit_distance <= max_edit_distance:
                        replacement_string_map[current_edit_distance-1][lexw] = self._pcfg.get_frequency(lexw)
                k = 0
                while k < max_edit_distance:
                    if len(replacement_string_map[k]) > 0:
                        break
                    else:
                        k += 1
                
                # Get replacement word with max frequency
                if k < max_edit_distance and len(replacement_string_map[k]) > 0:
                    ts = max(replacement_string_map[k], key=replacement_string_map[k].get)
                    print("Replaced with word: " + ts + ", edit dist=", k+1)
                else:
                    print("Skip word")
                    skip_word = True
                    n -= 1
            
            if not skip_word:
                current_row.append({})
                current_cell = current_row[i]
                
                # Add all {non-terminal: probability}
                # Get non-terminals that lead to this terminal
                for nts in self._pcfg.lexicon()[ts]:
                    current_max_log_proba = -np.inf
                    for trans, val in self._pcfg.root_to_trans(nts).items():
                        if np.log(val) > current_max_log_proba and trans.res_symb()[0].ssymb() == ts:
                            current_cell[nts] = (trans, np.log(val), ts_init)
                            current_max_log_proba = np.log(val)
                i += 1
            j += 1
        
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
        else:
            print("Failed to parse with CYK.")
        return None
        
