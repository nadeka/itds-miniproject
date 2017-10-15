###replace  +++$+++  with \t and save print conent as .tsv format as Kaggle 
def fileSplitIntoLines(filePath):
    fileLines = [line.rstrip('\n') for line in open(filePath)]
    for i in range(0, len(fileLines)):
        fileLines[i]=fileLines[i].replace(' +++$+++ ', '\t')
        print fileLines[i]
# fileSplitIntoLines('original/movie_characters_metadata.txt')      
# fileSplitIntoLines('original/movie_conversations.txt') 
# fileSplitIntoLines('original/movie_lines.txt')
# fileSplitIntoLines('original/movie_titles_metadata.txt')
### print to output to file e.g. python CleanUp.py > movie_characters_metadata.tsv

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
        ##remove /I from the year column
        df[df.columns[2]]=df[df.columns[2]].str.strip('/I')
        print 'After droping the votes column, shape is', df.shape
        df.columns = columnNames
        print df.head()
        df.to_csv('CleanUp/'+fileNameCleanUp, sep='\t', index=False, header =columnNames)
    elif(fileName=='movie_characters_metadata.tsv'):
        df = df.ix[:, 0:4]
        print 'After removing last column credit, shape is', df.shape
        df.columns = columnNames
        print df.head()
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
    print df.head()
    print df.shape
    print "*************Next New"
    return df
# lines=ReadFileWithHeader('CleanUp/movie_lines_cleanup.tsv')
# converstaions=ReadFileWithHeader('CleanUp/movie_conversations_cleanup.tsv')
# titles=ReadFileWithHeader('CleanUp/movie_titles_metadata_cleanup.tsv')
# characters=ReadFileWithHeader('CleanUp/movie_characters_metadata_cleanup.tsv')

############Note below method doesn't work well due to saving file either has "" or two tabs if escapechar='\t'
# import pandas as pd
# import csv
# def Data_preprocess(fileName, newfile):
    # data = pd.read_csv('original/'+fileName, sep='\t', header=None, error_bad_lines=False, warn_bad_lines=False)
    # print data.head()
    # print data.shape
    # data[0] = data[0].map(lambda x: x.replace(' +++$+++ ', '\t'))
    # print data.head()
    # print data.shape
    # ###saved file has two tabs between columns>>>not good
    # # data.to_csv(newfile, index=False,  header=None, quoting=csv.QUOTE_NONE,escapechar='\t')
	# ###below saved file has "" on rows =>>>>>>not good
    # data.to_csv(newfile, index=False,  header=None)
    # print "============Next file"
# chracter = Data_preprocess('movie_characters_metadata.txt', 'movie_characters_metadata.tsv')
# conversation = Data_preprocess('movie_conversations.txt', 'movie_conversations.tsv')
# lines = Data_preprocess('movie_lines.txt', 'movie_lines.tsv')
# titles = Data_preprocess('movie_titles_metadata.txt', 'movie_titles_metadata.tsv')
# urls = Data_preprocess('raw_script_urls.txt', 'raw_script_urls.tsv')

# df = pd.read_csv('movie_characters_metadata.tsv',sep='\t',header=None, error_bad_lines=False, warn_bad_lines=False)
# print 'After drop bad lines, shape is', df.shape
# print df.head()