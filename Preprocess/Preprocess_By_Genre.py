import pandas as pd
import os, re

movie_titles_df = pd.read_csv('..\CleanUp\movie_titles_metadata_cleanup.tsv',sep='\t',encoding='ISO-8859-2',warn_bad_lines =False,error_bad_lines=False,header=0)
movie_titles_df.columns = ['mId','movieTitle','movieYear','rating','geners']

conver_df = pd.read_csv('..\CleanUp\movie_conversations_cleanup.tsv',encoding='ISO-8859-2',warn_bad_lines =False,sep='\t',header=None)
lines_df = pd.read_csv('..\CleanUp\movie_lines_cleanup.tsv',sep='\t',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=None)

conver_df.columns = ['chId','chId2','mId','lines']
lines_df.columns = ['lineId','chId','mId','chName','dialogue']

# Split genres
def split_genres (genres):
   return (re.sub("[^a-zA-Z-]", " ", genres).split())

movie_titles_split_genres = movie_titles_df
movie_titles_split_genres.geners = movie_titles_df.geners.apply(split_genres)

# To get unique genres in alphabetical order. 
s = movie_titles_split_genres.apply(lambda x: pd.Series(x['geners']),axis=1).stack().reset_index(level=1, drop=True)
list_of_genres = sorted(list(set(s)))

if not os.path.exists('movie_titles_by_genre'):
    os.makedirs('movie_titles_by_genre')

if not os.path.exists('movie_lines_by_genre'):
    os.makedirs('movie_lines_by_genre')
	
if not os.path.exists('movie_conversations_by_genre'):
    os.makedirs('movie_conversations_by_genre')

for i in list_of_genres:
   movie_titles_by_genre = movie_titles_df[(movie_titles_df.geners.apply(lambda x: i in x))]
   movie_titles_by_genre.to_csv('movie_titles_by_genre\movie_titles_'+i+'.csv',index=False)
   df = pd.merge(lines_df, movie_titles_by_genre, how='inner', on=['mId'],left_index=False, right_index=False, suffixes=('_x', '_y'), copy=True, indicator=False)
   df=df.drop(['movieTitle','movieYear','rating','geners'],axis=1)
   df.to_csv('movie_lines_by_genre\movie_lines_'+i+'.tsv',index=False,sep='\t')
   df2 = pd.merge(conver_df, movie_titles_by_genre, how='inner', on=['mId'],left_index=False, right_index=False, suffixes=('_x', '_y'), copy=True, indicator=False)
   df2=df2.drop(['movieTitle','movieYear','rating','geners'],axis=1)
   df2.to_csv('movie_conversations_by_genre\movie_conversations_'+i+'.tsv',index=False,sep='\t')