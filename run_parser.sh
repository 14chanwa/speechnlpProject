#!/bin/bash
# Usage: ./run_parser.sh "Amélioration de la sécurité\nGutenberg"
# Sample output:
#~ n_train= 2480 n_dev= 310 n_test= 310
#~ 3464 non-terminals
#~ 8342 words
#~ >>> Parsing: Amélioration de la sécurité
#~ (SENT (NC amélioration) (PP (P de) (NP (DET la) (NC sécurité))))
#~ >>> Parsing: Gutenberg
#~ (SENT gutenberg)

python test_main.py "$@"
