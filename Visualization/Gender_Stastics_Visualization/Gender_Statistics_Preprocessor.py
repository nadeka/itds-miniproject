import pandas as pd

lines_df = pd.read_csv('..\..\CleanUp\movie_lines_cleanup.tsv',sep='\t',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)
lines_df.columns = ['lineId','chId','mId','chName','dialogue']

characters_df = pd.read_csv('..\..\CleanUp\movie_characters_metadata_cleanup.tsv',sep='\t',encoding='ISO-8859-2',warn_bad_lines =False,error_bad_lines=False,header=0)
characters_df.columns=['chId','chName','mId','mName','gender']

# let's join lines_df and characters_df together so that we can know if a line was uttered by which gender.
df = pd.merge(lines_df, characters_df, how='inner', on=['chId','mId','chName'],left_index=False, right_index=False, sort=True,suffixes=('_x', '_y'), copy=True,indicator=False)

#Overall Movie_Titles
movie_titles_df = pd.read_csv('..\..\CleanUp\movie_titles_metadata_cleanup.tsv',sep='\t',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)
movie_titles_df.columns = ['mId','movieTitle','movieYear','rating','geners']



movie_titles_df_original_percentages = movie_titles_df
# Count numbe rof female dialogues, male dialogues, ? dialogues..make a function for this so that as a return to this function..three columns are appended to the data which # number of dialogues each

movie_titles_df_original_percentages['female_lines_count']= movie_titles_df_original_percentages.mId.apply(lambda x: df[(df.mId==x)&((df.gender=='f')| (df.gender=='F'))].mId.count())
movie_titles_df_original_percentages['male_lines_count']= movie_titles_df_original_percentages.mId.apply(lambda x: df[(df.mId==x)&((df.gender=='m')| (df.gender=='M'))].mId.count())
movie_titles_df_original_percentages['unknown_lines_count']= movie_titles_df_original_percentages.mId.apply(lambda x: df[(df.mId==x)&(df.gender=='?')].mId.count())


# Calculate percentages
movie_titles_df_original_percentages['female_lines_percentage'] = (movie_titles_df_original_percentages['female_lines_count']/(movie_titles_df_original_percentages['female_lines_count']+movie_titles_df_original_percentages['male_lines_count']+movie_titles_df_original_percentages['unknown_lines_count']))*100
movie_titles_df_original_percentages['male_lines_percentage'] = (movie_titles_df_original_percentages['male_lines_count']/(movie_titles_df_original_percentages['female_lines_count']+movie_titles_df_original_percentages['male_lines_count']+movie_titles_df_original_percentages['unknown_lines_count']))*100
movie_titles_df_original_percentages['unknown_lines_percentage'] = (movie_titles_df_original_percentages['unknown_lines_count']/(movie_titles_df_original_percentages['female_lines_count']+movie_titles_df_original_percentages['male_lines_count']+movie_titles_df_original_percentages['unknown_lines_count']))*100

movie_titles_df_original_percentages.to_csv('Original_Dialogue_Percentages.csv',index=False)


####Work with Imputed Genders Data###
characters_df_imputed = pd.read_csv('..\..\CleanUp\movie_characters_metadata_cleanup_gender.tsv',sep='\t',encoding='ISO-8859-2',warn_bad_lines =False,error_bad_lines=False,header=0)
characters_df_imputed.columns=['chId','chName','mId','mName','gender']

# let's join lines_df and characters_df together so that we can know if a line was uttered by which gender.
df_imputed = pd.merge(lines_df, characters_df_imputed, how='inner', on=['chId','mId','chName'],left_index=False, right_index=False, sort=True,suffixes=('_x', '_y'), copy=True,indicator=False)

movie_titles_df_imputed_percentages = movie_titles_df
# Count numbe rof female dialogues, male dialogues, ? dialogues..make a function for this so that as a return to this function..three columns are appended to the data which # number of dialogues each

movie_titles_df_imputed_percentages['female_lines_count']= movie_titles_df_imputed_percentages.mId.apply(lambda x: df_imputed[(df_imputed.mId==x)&((df_imputed.gender=='f')| (df_imputed.gender=='F'))].mId.count())
movie_titles_df_imputed_percentages['male_lines_count']= movie_titles_df_imputed_percentages.mId.apply(lambda x: df_imputed[(df_imputed.mId==x)&((df_imputed.gender=='m')| (df_imputed.gender=='M'))].mId.count())
movie_titles_df_imputed_percentages['unknown_lines_count']= movie_titles_df_imputed_percentages.mId.apply(lambda x: df_imputed[(df_imputed.mId==x)&(df_imputed.gender=='?')].mId.count())


# Calculate percentages
movie_titles_df_imputed_percentages['female_lines_percentage'] = (movie_titles_df_imputed_percentages['female_lines_count']/(movie_titles_df_imputed_percentages['female_lines_count']+movie_titles_df_imputed_percentages['male_lines_count']+movie_titles_df_imputed_percentages['unknown_lines_count']))*100
movie_titles_df_imputed_percentages['male_lines_percentage'] = (movie_titles_df_imputed_percentages['male_lines_count']/(movie_titles_df_imputed_percentages['female_lines_count']+movie_titles_df_imputed_percentages['male_lines_count']+movie_titles_df_imputed_percentages['unknown_lines_count']))*100
movie_titles_df_imputed_percentages['unknown_lines_percentage'] = (movie_titles_df_imputed_percentages['unknown_lines_count']/(movie_titles_df_imputed_percentages['female_lines_count']+movie_titles_df_imputed_percentages['male_lines_count']+movie_titles_df_imputed_percentages['unknown_lines_count']))*100

movie_titles_df_imputed_percentages.to_csv('Imputed_Dialogue_Percentages.csv',index=False)