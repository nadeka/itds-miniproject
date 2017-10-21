## First install http://landinghub.visualstudio.com/visual-cpp-build-tools for WordCloud
## Go To Anconda and pip install WordCloud
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


import warnings
warnings.filterwarnings('ignore')

#Go to folder which contains the TSV files
conver_df = pd.read_csv('..\..\CleanUp\movie_conversations_cleanup.tsv',encoding='ISO-8859-2',warn_bad_lines =False,sep='\t',header=None)
lines_df = pd.read_csv('..\..\CleanUp\movie_lines_cleanup.tsv',sep='\t',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=None)
characters_df = pd.read_csv('..\..\CleanUp\movie_characters_metadata_cleanup.tsv',encoding='ISO-8859-2',sep='\t',warn_bad_lines =False,error_bad_lines=False,header=None)

# Characters_df contains metadata about characters and the movie he/she is in
characters_df.columns=['chId','chName','mId','mName','gender']
characters_df.head()

# Conver_df contains conversation between two characters.
conver_df.columns = ['chId','chId2','mId','lines']
conver_df.head()

lines_df.columns = ['lineId','chId','mId','chName','dialogue']
lines_df.head()

# let's join lines_df and characters_df together so that we can know the name of the movie the character is in.
print ("Merging lines data frame and character dataframe")
df = pd.merge(lines_df, characters_df, how='inner', on=['chId','mId','chName'],
		 left_index=False, right_index=False, sort=True,
		 suffixes=('_x', '_y'), copy=True, indicator=False)
df.head()

# text Cleaning and Preprocessing
#Select only dialogue that is not null
df = df[df['dialogue'].notnull()]

wordnet_lemmatizer = WordNetLemmatizer()
def clean_dialogue( dialogue ):
	# Function to convert a raw review to a string of words
	# The input is a single string (a raw movie review), and 
	# the output is a single string (a preprocessed movie review)
	#
	# 1. Remove HTML
	#
	# 2. Remove non-letters        
	letters_only = re.sub("[^a-zA-Z]", " ", dialogue) 
	#
	# 3. Convert to lower case, split into individual words
	words = letters_only.lower().split()                             
	#
	# 4. In Python, searching a set is much faster than searching
	#   a list, so convert the stop words to a set
	stops = set(stopwords.words("english"))   
	
	# 5. Use lemmatization and remove stop words
	meaningful_words = [wordnet_lemmatizer.lemmatize(w) for w in words if not w in stops]   
	#
	# 6. Join the words back into one string separated by space, 
	# and return the result.
	return( " ".join( meaningful_words ))
	
print ("Cleaning Dialogues")
df['cleaned_dialogue'] = df['dialogue'].apply(clean_dialogue)

df[['cleaned_dialogue','dialogue']].head()

df.to_csv('WordCloudPreprocessed.csv',index=False)