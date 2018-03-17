# speechnlpProject


Implements a grammar parser for Natural Language Processing using probabilistic CFGs and the CYK algorithm. This is a homework for the [Speech and Natural Language Processing course](https://github.com/edupoux/MVA_2018_SL) of the [Master MVA](http://math.ens-paris-saclay.fr/version-francaise/formations/master-mva/), taught by E. Dupoux and B. Sagot. 


The goal of the first part is to build a parser that learn CFG (context-free grammar) rules from a learning corpus (in this case the [Sequoia Treebank](https://www.rocq.inria.fr/alpage-wiki/tiki-index.php?page=CorpusSequoia)) and build a PCFG (probabilistic CFG), i.e. a CFG with rules `A->B` given a probability of occurrence among all transitions `A->X`. An input example would be for instance:
```
( (SENT (NP (NC Amélioration) (PP (P de) (NP (DET la) (NC sécurité))))))
```
The algorithm builds a CFG in Chomsky normal form (this is necessary for the algorithm to perform the second part of the homework). A tricky case is for instance:
```
( (SENT (NP (NPP Gutenberg))))
```
where, for CYK to work, one can decide to add all the possible rules, i.e.
```
SENT->NP
NP->NPP
NPP->Gutenberg
NP->Gutenberg
SENT->Gutenberg
```


The second part consists in a parser which returns a CFG-parsed version of an input sentence. For instance, the input 
```
Amélioration de la sécurité
```
would return
```
(SENT (NC amélioration) (PP (P de) (NP (DET la) (NC sécurité))))
```
This part makes use of the PCFG built from the training corpus in order to derive the CFG parsing. It is mainly based on recognizing the different terminals (words) and deriving the most probable CFG parsing using dynamic programming (with a modified CYK algorithm).


## How to get the Sequoia Treebank v6.0


Go to the Inria [download interface](https://gforge.inria.fr/frs/?group_id=3597&release_id=9064). Unzip the file `sequoia-corpus-v6.0.tgz` and place the file `sequoia-corpus+fct.mrg_strict` in this folder.


## Parameters


Run the parser with the file `run_parser.sh`. The first parameter should be a string to be parsed. Each sentence should be separated by `\n`, each word should be separated by a white space.


No other parameter, the program will read the training corpus `sequoia-corpus+fct.mrg_strict`. This file should remain in this folder.


Note that this script learns the PCFG at each run.


## Example 


`chmod+x run_parser.sh & ./run_parser.sh "Amélioration de la sécurité\nGutenberg"`


Sample output:

```
n_train= 2480 n_dev= 310 n_test= 310
3464 non-terminals
8342 words
>>> Parsing: Amélioration de la sécurité
(SENT (NC amélioration) (PP (P de) (NP (DET la) (NC sécurité))))
>>> Parsing: Gutenberg
(SENT gutenberg)
```

