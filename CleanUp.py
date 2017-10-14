import pandas as pd
movie_lines_columns = ["lineID", "characterID", "movieID", "characterName", "utteranceText"]
movie_conversations_columns = ["characterID1", "characterID2", "movieID", "utteranceTextList"]
movie_titles_metadata_columns = ["movieID", "movieTitle", "movieYear", "rating", "geners"]
movie_characters_metadata_columns = ["characterID", "characterName", "movieID", "movieTitle", "gender"]
def CleanUp(fileName, fileNameCleanUp, columnNames):
    df = pd.read_csv(fileName,sep='\t',header=None, error_bad_lines=False, warn_bad_lines=False)
    print 'After drop bad lines, shape is', df.shape
    df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    print 'After removing rows with NAN, shape is', df.shape
    if(fileName=='movie_titles_metadata.tsv'):
        df.drop(df.columns[4], axis=1, inplace=True)
        print 'After droping the votes column, shape is', df.shape
        df.columns = columnNames
        df.to_csv('CleanUp/'+fileNameCleanUp, sep='\t', index=False, header =columnNames)
    elif(fileName=='movie_characters_metadata.tsv'):
        df = df.ix[:, 0:4]
        print 'After removing last column credit, shape is', df.shape
        df.columns = columnNames
        df.to_csv('CleanUp/'+fileNameCleanUp, sep='\t', index=False, header =columnNames)
    else:
        df.columns = columnNames
        print df.head()
        df.to_csv('CleanUp/'+fileNameCleanUp, sep='\t', index=False, header =columnNames)
    print "=============Next"
CleanUp('movie_lines.tsv', 'movie_lines_cleanup.tsv', movie_lines_columns)
CleanUp('movie_conversations.tsv', 'movie_conversations_cleanup.tsv', movie_conversations_columns)
CleanUp('movie_titles_metadata.tsv', 'movie_titles_metadata_cleanup.tsv', movie_titles_metadata_columns)
CleanUp('movie_characters_metadata.tsv', 'movie_characters_metadata_cleanup.tsv', movie_characters_metadata_columns)

def ReadFileWithHeader(file):
    df=pd.read_csv(file,sep='\t',header=0, error_bad_lines=False, warn_bad_lines=False)
    print df[0:5]
    print df.shape
    print "*************Next New"
    return df
lines=ReadFileWithHeader('CleanUp/movie_lines_cleanup.tsv')
converstaions=ReadFileWithHeader('CleanUp/movie_conversations_cleanup.tsv')
titles=ReadFileWithHeader('CleanUp/movie_titles_metadata_cleanup.tsv')
characters=ReadFileWithHeader('CleanUp/movie_characters_metadata_cleanup.tsv')

