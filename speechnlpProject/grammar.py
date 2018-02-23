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
        if stype not in [NON_TERMINAL, TERMINAL]:
            raise Exception("Unrecognized symbol type")
        self._stype = stype

    
    def __eq__(self, gsymb):
        return self._ssymb == gsymb._ssymb and \
            self._stype == gsymb._stype

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
        self._tgsymb = tgsymb
        
    
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
        GSymbol.symb
        Get the root symbol.
        
        Returns
        ----------
        ssymb: GSymbol.
    """
    def symb(self):
        return self._gsymb
    
    
    """
        GSymbol.is_chomsky_normal_form
        Checks if the transition is in a Chomsky normal form.
        
        Returns
        ----------
        res: bool.
    """
    def is_chomsky_normal_form(self):
        
        if len(self._tgsymb) < 2:
            return True
        if len(self._tgsymb) > 2:
            return False
        if self._tgsymb[0].stype() == GSymbol.TERMINAL:
            return False
        return True
    
    
    """
        GSymbol.to_chomsky_normal_form
        Transforms the transition in a Chomsky normal form.
        Creates substitutes GSymbols in order to make intermediate
        transitions.
        
        Returns
        ----------
        chomsky_normal_form: list(GTransition).
            A list of transitions in a Chomsky normal form replacing the
            current transitions.
    """
    def to_chomsky_normal_form(self):
        
        chomsky_normal_form = [self]
        
        if self.is_chomsky_normal_form():
            return chomsky_normal_form
        
        else:
            
            # Assume transitions NT -> NT do not exist...
            # TODO what if they do
            
            # Replace T by NT
            for i in range(len(self._tgsymb)):
                if self._tgsymb[i].stype() == GSymbol.TERMINAL:
                    # Make new symbol
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
                    chomsky_normal_form.append(new_trans)
            
            # Each transition should lead to at most 2 NT
            # Begin from the end
            current_index = len(self._tgsymb) - 1
            while current_index > 1: # Stop when there are 2 NTs left
                
                # Get current and previous NTs and merge them into one
                # combined NT
                # Make new symbol
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
                self._tgsymb.pop(-1)
                self._tgsymb[-1] = new_symb
                # Add the newly created transition
                chomsky_normal_form.append(new_trans)
                
                current_index -= 1
            
            
            return chomsky_normal_form


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

    Returns
    ----------
    nts: Counter({GTransition : n}).
        Counter of different transitions.
"""
    def __init__(self, counter_gtrans, chomsky_normalize=False):
        # If option selected
        if chomsky_normalize:
            # For each gtrans, normalize gtrans
            normalized_counter_gtrans = Counter()
            for key, value in counter_gtrans.items():
                if key.is_chomsky_normal_form():
                    #~ print("est_chomsky:", key)
                    normalized_counter_gtrans[key] = value
                else:
                    normalized_form = key.to_chomsky_normal_form()
                    for elt in normalized_form:
                        if not elt in normalized_counter_gtrans.keys():
                            normalized_counter_gtrans[elt] = 0
                        normalized_counter_gtrans[elt] += value
                        #~ print(elt, normalized_counter_gtrans[elt])
        else:
            normalized_counter_gtrans = counter_gtrans
        
        cfgmap = {}
        
        # Create map
        for key, value in normalized_counter_gtrans.items():
            gsymb = key.symb()
            if not gsymb in cfgmap.keys():
                cfgmap[gsymb] = {}
            cfgmap[gsymb][key] = value
        
        # Compute probabilities by key
        for key, value in cfgmap.items():
            sum_counts = sum(value.values())
            for key2, value2 in value.items():
                value[key2] = value2 / sum_counts
        self._cfgmap = cfgmap
    
    
    """
        PCFG.__repr__
        Maps PCFG to a description string. Lists symbol + related
        transitions.        
        
        res: string.
    """
    def __repr__(self):
        
        res = ""
        
        for gsymb in self.symbs():
            res += ">>>\t" + str(gsymb) + "\n"
            for trans, value in self.trans(gsymb).items():
                res += "\t" + "{0:.2f}".format(value) + "\t" + str(trans) + "\n"
        
        return res[:len(res)-1]
    
    
    """
        GSymbol.symbs
        Get the grammar symbols.
        
        Returns
        ----------
        ssymbs: list(GSymbol).
    """
    def symbs(self):
        return self._cfgmap.keys()
    
    
    """
        GSymbol.trans
        Get the grammar transitions with root the provided symbol.
        
        Parameters
        ----------
        gsymb: GSymbol.
        
        Returns
        ----------
        strans: list(GSymbol).
    """
    def trans(self, gsymb):
        return self._cfgmap[gsymb]
