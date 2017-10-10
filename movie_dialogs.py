import pandas as pd

lines = pd.read_csv('movie_lines.tsv', sep='\t', header=None, error_bad_lines=False, warn_bad_lines=True)
dialogs = pd.read_csv('movie_conversations.tsv', sep='\t', header=None, error_bad_lines=False, warn_bad_lines=True)
movie_metadata = pd.read_csv('movie_titles_metadata.tsv', sep='\t', header=None, error_bad_lines=False, warn_bad_lines=True)
character_metadata = pd.read_csv('movie_characters_metadata.tsv', sep='\t', header=None, error_bad_lines=False, warn_bad_lines=True)
