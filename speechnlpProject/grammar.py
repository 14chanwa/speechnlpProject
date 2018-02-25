# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:58:06 2018

@author: Quentin
"""

from collections import Counter


"""
    GSymbol
    Implements grammatical symbol.
"""
class GSymbol:
    
    
    NON_TERMINAL = 0
    TERMINAL = 1
    
    
    """
        GSymbol.__init__
        Builds a symbol.
        
        Parameters
        ----------
        ssymb: string. 
            The unique identifier of the symbol.
        stype: int (NON_TERMINAL or TERMINAL).
            The type NON_TERMINAL (0) or TERMINAL (1) of the symbol.
    """
    def __init__(self, ssymb, stype):
        self._ssymb = ssymb
        if stype not in [self.NON_TERMINAL, self.TERMINAL]:
            raise Exception("Unrecognized symbol type")
        self._stype = stype

    
    def __eq__(self, gsymb):
        return self._ssymb == gsymb._ssymb and \
            self._stype == gsymb._stype
    
    
    def __lt__(self, a):
        return self._ssymb < a._ssymb
    

    """
        GSymbol.__repr__
        Map GSymbol to string symbol.
        
        res: string.
    """
    def __repr__(self):
        return self._ssymb


    def __hash__(self):
        return hash((self._ssymb, self._stype))

    """
        GSymbol.ssymb
        Get the symbol.
        
        Returns
        ----------
        ssymb: string.
    """
    def ssymb(self):
        return self._ssymb
    
    """
        GSymbol.stype
        Get the type.
        
        Returns
        ----------
        stype: int (NON_TERMINAL or TERMINAL).
    """
    def stype(self):
        return self._stype


"""
    GTransition
    Implements grammatical transition.
"""
class GTransition:
    
    # Index statically used to name new variables created by the
    # Chomsky normalization process
    _chomsky_variable_index = 1
    
    # Map very long names like NP_PONCT_NP_PONCT_VN_NP to short names 
    # like X53. Useful to avoid duplicate variables.
    _transition_name_mapper = {}
    
    """
        GSymbol.__init__
        Builds a transition.
        
        Parameters
        ----------
        gsymb: GSymbol. 
            The root symbol of the transition.
        tgsymb: list(GSymbol).
            An ordered list of the symbols of the result of the transition.
    """
    def __init__(self, gsymb, tgsymb):
        
        if gsymb._stype == GSymbol.TERMINAL:
            raise Exception("Cannot make GTransition from terminal symbol")
        
        
        self._gsymb = gsymb
        self._tgsymb = tuple(tgsymb)
        
    
    def __eq__(self, gtrans):
        
        if self._gsymb != gtrans._gsymb:
            return False
        if len(self._tgsymb) != len(gtrans._tgsymb):
            return False
        for i in range(len(self._tgsymb)):
            if self._tgsymb[i] != gtrans._tgsymb[i]:
                return False
        return True
    
    
    """
        GTransition.__repr__
        Maps GTransition to a description string. 
        
        res: string.
    """
    def __repr__(self):
        
        res = str(self._gsymb) + " -> "
        for gsymb in self._tgsymb:
            res += str(gsymb) + " "
        return res[:len(res)-1]
    
    
    def __hash__(self):
        
        return hash(((self._gsymb), tuple(self._tgsymb)))
    
    
    """
        GTransition.symb
        Get the root symbol.
        
        Returns
        ----------
        gsymb: GSymbol.
    """
    def symb(self):
        return self._gsymb
    
    
    """
        GTransition.res_symb
        Get the result list of symbols.
        
        Returns
        ----------
        res_symb: GSymbol.
    """
    def res_symb(self):
        return self._tgsymb
    
    
    """
        GTransition.symb
        Get the transition symbols.
        
        Returns
        ----------
        tgsymb: tuple(GSymbol).
    """
    def transition_symb(self):
        return self._tgsymb
    
    
    """
        GTransition.is_chomsky_normal_form
        Checks if the transition is in a Chomsky normal form.
        
        Returns
        ----------
        res: bool.
    """
    def is_chomsky_normal_form(self):
        
        if len(self._tgsymb) > 2:
            return False
        if len(self._tgsymb) == 2 and self._tgsymb[0].stype() == GSymbol.TERMINAL:
            return False
        if self._tgsymb[0].stype() == GSymbol.NON_TERMINAL:
            return False
        return True
    
    
    """
        GTransition.reduce_to_2_or_less
        Transforms the transition in a Chomsky normal form.
        Creates substitutes GSymbols in order to make intermediate
        transitions.
        
        Returns
        ----------
        new_trans_list: list(GTransition).
            A list of transitions in a Chomsky normal form replacing the
            current transitions.
    """
    def reduce_to_2_or_less(self, short_name=True):
        
        new_trans_list = [self]
        
        if len(self.transition_symb()) <= 2:
            return new_trans_list
        
        else:
            
            # Assume transitions NT -> NT do not exist...
            # TODO what if they do
            
            # Replace T by NT
            for i in range(len(self._tgsymb)):
                if self._tgsymb[i].stype() == GSymbol.TERMINAL:
                    # Make new symbol
                    #~ new_symb = GSymbol(\
                        #~ "X" + str(_chomsky_variable_index), \
                        #~ GSymbol.NON_TERMINAL\
                        #~ )
                    #~ GTransition._chomsky_variable_index += 1
                    new_symb = GSymbol(\
                        "t[" + self._tgsymb[i].ssymb() + "]", \
                        GSymbol.NON_TERMINAL\
                        )
                    # Make new transition
                    new_trans = GTransition(\
                        new_symb,\
                        [self._tgsymb[i]]\
                        )
                    # Replace old terminal by new non-terminal
                    self._tgsymb[i] = new_symb
                    # Append new transition
                    new_trans_list.append(new_trans)
            
            # Each transition should lead to at most 2 NT
            # Begin from the end
            current_index = len(self._tgsymb) - 1
            while current_index > 1: # Stop when there are 2 NTs left
                
                # Get current and previous NTs and merge them into one
                # combined NT
                # Make new symbol
                
                # This is a unique key for the current transition (for
                # instance, "NP_PONCT_NP_PONCT_VN_NP"), but very long..
                transition_key = \
                    self._tgsymb[current_index - 1].ssymb() + "_" + \
                    self._tgsymb[current_index].ssymb()
                
                if short_name:
                    # Create a short key if no existent key
                    if transition_key not in GTransition._transition_name_mapper.keys():
                        GTransition._transition_name_mapper[transition_key] = \
                            "X" + str(GTransition._chomsky_variable_index)
                        GTransition._chomsky_variable_index += 1
                    
                    new_symb = GSymbol(\
                            GTransition._transition_name_mapper[transition_key], \
                            GSymbol.NON_TERMINAL\
                            )
                else:
                    new_symb = GSymbol(\
                            self._tgsymb[current_index - 1].ssymb() + "_" + 
                            self._tgsymb[current_index].ssymb(), \
                            GSymbol.NON_TERMINAL\
                            )
                # Make new transition
                new_trans = GTransition(\
                        new_symb,\
                        [self._tgsymb[current_index-1], self._tgsymb[current_index]]\
                        )
                # Replace NTs into base transition
                new_tgsymb = list(self._tgsymb)
                new_tgsymb.pop(-1)
                new_tgsymb[-1] = new_symb
                self._tgsymb = tuple(new_tgsymb)
                # Add the newly created transition
                new_trans_list.append(new_trans)
                
                current_index -= 1
            
            
            return new_trans_list


"""
    PCFG
    Implements probabilistic context-free grammars.
"""
class PCFG:
    
    """
    PCFG.__init__
    Build a PCFG model (a map {NT GSymbol, {GTransition, proba}}

    Parameters
    ----------
    counter_gtrans: Counter(GTransition, int). 
        A Counter of the GTransitions and their number of apparitions
        in the parsed corpus.
    chomsky_normalize=False: bool.
        Optional. Performs or not a Chomsky normalization.
    short_name=True:bool.
        Optional. Useful if Chomsky normalization: use short names like
        "X451" instead of "NP_PONCT_NP_PONCT_VN_NP" for instance.
"""
    def __init__(self, counter_gtrans, chomsky_normalize=False, \
                            short_name=True):
        # If option selected
        if chomsky_normalize:
            
            
            # For each gtrans, reduce to transitions of length 2 or less
            normalized_counter_gtrans = Counter()
            for key, value in counter_gtrans.items():
                if len(key.transition_symb()) <= 2:
                    #~ print("est_chomsky:", key)
                    normalized_counter_gtrans[key] = value
                else:
                    normalized_form = key.reduce_to_2_or_less(short_name)
                    for elt in normalized_form:
                        if not elt in normalized_counter_gtrans.keys():
                            normalized_counter_gtrans[elt] = 0
                        normalized_counter_gtrans[elt] += value
                        #~ print(elt, normalized_counter_gtrans[elt])
            
            
            #~ # For each gtrans, if length == 1 and non-terminal symbol,
            #~ # replace the results by the next res level
            #~ while True:
                
                #~ print("loop")
                
                #~ normalized = True
                
                #~ # Search for a transition to remove
                #~ for trans in normalized_counter_gtrans.keys():
                    
                    #~ trans2 = trans
                    
                    #~ if len(trans2.res_symb()) == 1 and \
                        #~ trans2.res_symb()[0].stype() == GSymbol.NON_TERMINAL:
                        
                        #~ normalized = False
                        #~ trans2._tgsymb = 
                        
                        #~ print("stub")
                        
                        #~ normalized = False
                            
                        #~ # Remove this transition
                        #~ symbol_to_replace = trans.symb()
                        #~ target_symbol = trans.res_symb()[0]
                        
                        #~ normalized_counter_gtrans_2 = {}
                        #~ for trans2, value in normalized_counter_gtrans.items():
                            #~ if trans2 != trans:
                                #~ for i in range(len(trans2.res_symb())):
                                    #~ new_symb_list = list(trans2.res_symb())
                                    #~ if new_symb_list[i] == symbol_to_replace:
                                        #~ new_symb_list[i] = target_symbol
                                        #~ print(trans2)
                                        #~ print("la")
                                    #~ trans2._tgsymb = tuple(new_symb_list)
                        
                        
                        #~ print("removed transition:", symbol_to_replace, "->", target_symbol)
                        
                        #~ print("break")
                        #~ break
                    #~ if trans2 in normalized_counter_gtrans_2.keys():
                        #~ normalized_counter_gtrans_2[trans2] += value
                    #~ else:
                        #~ normalized_counter_gtrans_2[trans2] = value
                        
                    
                #~ normalized_counter_gtrans = normalized_counter_gtrans_2
                    
                #~ if normalized:
                    #~ break
                #~ else:
                    #~ print("continue")
                    #~ continue
            
            
        else:
            normalized_counter_gtrans = counter_gtrans
        
        cfgmap = {}
        
        # Create map & lexicon
        self._lexicon = {}
        
        for key, value in normalized_counter_gtrans.items():
            gsymb = key.symb()
            if not gsymb in cfgmap.keys():
                cfgmap[gsymb] = {}
            cfgmap[gsymb][key] = value
            
            # Add terminal to the lexicon
            if len(key.transition_symb()) == 1 and \
                    key.transition_symb()[0].stype() == GSymbol.TERMINAL:
                if key.transition_symb()[0].ssymb() not in \
                        self._lexicon.keys():
                    self._lexicon[key.transition_symb()[0].ssymb()] = set()
                self._lexicon[key.transition_symb()[0].ssymb()].add(key.symb())
        
        # Compute probabilities by key
        for key, value in cfgmap.items():
            sum_counts = sum(value.values())
            for key2, value2 in value.items():
                value[key2] = value2 / sum_counts
        self._cfgmap = cfgmap
    
    
        # Build an inverse map result to transition
        # for instance A -> B, C will be mapped [B, C] -> {(A -> B, C): p}
        self._cfg_inversemap = {}
        for gtrans_proba in self._cfgmap.values():
            for gtrans in gtrans_proba.keys():
                res_symb = gtrans.res_symb()
                if res_symb not in self._cfg_inversemap.keys():
                    self._cfg_inversemap[res_symb] = {}
                self._cfg_inversemap[res_symb][gtrans] = gtrans_proba[gtrans]
                
    
    """
        PCFG.__repr__
        Maps PCFG to a description string. Lists symbol + related
        transitions.        
        
        res: string.
    """
    def __repr__(self):
        
        res = ""
        
        for gsymb in self.nt_symbs():
            res += ">>>\t" + str(gsymb) + "\n"
            for trans, value in self.root_to_trans(gsymb).items():
                res += "\t" + "{0:.2f}".format(value) + "\t" + str(trans) + "\n"
        
        return res[:len(res)-1]
    
    
    """
        PCFG.nt_symbs
        Get the grammar non-terminal symbols.
        
        Returns
        ----------
        ssymbs: list(GSymbol).
    """
    def nt_symbs(self):
        return sorted(list(self._cfgmap.keys()))
    
    
    """
        PCFG.root_to_trans
        Get the grammar transitions with root the provided symbol.
        
        Parameters
        ----------
        gsymb: GSymbol.
        
        Returns
        ----------
        d_gtrans: dict{GTransition: probability}.
    """
    def root_to_trans(self, gsymb):
        return self._cfgmap[gsymb]
    
    
    """
        PCFG.res_to_trans
        Get the grammar transitions with result the provided list of
        symbols.
        
        Parameters
        ----------
        l_gsymb: tuple(GSymbol).
        
        Returns
        ----------
        d_gtrans: dict{GTransition: probability}.
    """
    def res_to_trans(self, l_gsymb):
        if l_gsymb in self._cfg_inversemap.keys():
            return self._cfg_inversemap[l_gsymb]
        return {}
    
    
    """
        PCFG.lexicon
        Get the lexicon (mapping word -> set of possible corresponding
        non-terminals).
        
        Returns
        ----------
        lexicon: dict{String : set(GSymbol(Non-Terminal))}.
    """
    def lexicon(self):
        return self._lexicon
