# -*- coding: utf-8 -*-
import pandas as pd
from ast import literal_eval

movie_lines = pd.read_csv('../CleanUp/movie_lines_cleanup.tsv', sep='\t', encoding='latin-1', header=None, error_bad_lines=False, warn_bad_lines=False)
movie_dialogs = pd.read_csv('../CleanUp/movie_conversations_cleanup.tsv', sep='\t', encoding='latin-1', header=None, error_bad_lines=False, warn_bad_lines=False)

dialogs = movie_dialogs.iloc[1:, 3:4]

# Fetch lines corresponding to given line ids in correct order
# Return result in following string form:
# CHAR1  <line>
# CHAR2  <line>
# ...    ...
def get_lines(lines_list):
    lines = []
    
    for l in lines_list:
        line = movie_lines.loc[movie_lines[0] == l].iloc[:, 3:5].values
        
        if len(line) > 0 and len(line[0]) > 0 and line[0][0] and line[0][1]:
            lines.append(line[0][0] + '\t' + line[0][1])
    
    return '\n'.join(lines)
    
# Write dialogs to input file in RNN library folder
with open('char-rnn-tensorflow-master/data/dialogs/input.txt', 'w', encoding='utf-8') as f: 
    dialogs.apply(lambda d: f.write(get_lines(literal_eval(d.values[0])) + '\n\n'), axis=1)
