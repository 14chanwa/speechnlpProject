# speechnlpProject


Implementation of a PCFG and probabilistic CYK.


### Parameters


First parameter should be a string to be parsed. Each sentence should be separated by `\n`, each word should be separated by a white space.


No other parameter, the program will read the training corpus `sequoia-corpus+fct.mrg_strict`. This file should stay in this folder.


### Example 


`chmod+x run_parser.sh & ./run_parser.sh "Amélioration de la sécurité\nGutenberg"`


Sample output:

`
n_train= 2480 n_dev= 310 n_test= 310
3464 non-terminals
8342 words
>>> Parsing: Amélioration de la sécurité
(SENT (NC amélioration) (PP (P de) (NP (DET la) (NC sécurité))))
>>> Parsing: Gutenberg
(SENT gutenberg)
`
