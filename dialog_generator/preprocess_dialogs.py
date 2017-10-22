# -*- coding: utf-8 -*-
import pandas as pd
import os
from ast import literal_eval

movie_dialogs = pd.read_csv('../CleanUp/movie_conversations_cleanup.tsv', sep='\t', encoding='latin-1', 
                            header=0, error_bad_lines=False, warn_bad_lines=False)
movie_lines = pd.read_csv('../CleanUp/movie_lines_cleanup.tsv', sep='\t', encoding='latin-1', 
                          header=0, error_bad_lines=False, warn_bad_lines=False)
movie_titles = pd.read_csv('../CleanUp/movie_titles_metadata_cleanup.tsv', sep='\t', encoding='latin-1', 
                           header=0, error_bad_lines=False, warn_bad_lines=False)

genres = ['comedy', 'action', 'drama']
rating_ranges = {'low': [0.0, 5.9], 'mid': [6.0, 7.4], 'high': [7.5, 10.0]}


# Fetch lines corresponding to given line ids in correct order
# Return result in following string form:
# CHAR1  <line>
# CHAR2  <line>
# ...    ...
def get_lines(lines_list):
    lines = []
    
    for l in lines_list:
        line = movie_lines.loc[movie_lines['lineID'] == l].iloc[:, 3:5].values
        
        if len(line) > 0 and len(line[0]) > 0 and line[0][0] and line[0][1]:
            lines.append(str(line[0][0]) + '\t' + str(line[0][1]))
    
    return '\n'.join(lines)


# Create input file for every genre + rating combination
for g in genres:
    # Filter movies by genre
    movies_by_g = movie_titles[movie_titles['geners'].apply(lambda x: g in literal_eval(x))]
            
    for key, val in rating_ranges.items():
        # Filter movies by rating
        movies_by_r = movies_by_g.loc[movies_by_g['rating'] >= val[0]]
        movies_by_r = movies_by_r.loc[movies_by_r['rating'] <= val[1]]
                
        if len(movies_by_r) > 0:
            dialogs = movie_dialogs.loc[movie_dialogs['movieID'].isin(movies_by_r['movieID'])].iloc[:, 3:4]

            filename = 'char_rnn_tensorflow_master/data/' + g + '_' + key + '/input.txt'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                dialogs.apply(lambda d: f.write(get_lines(literal_eval(d.values[0])) + '\n\n'), axis=1)
