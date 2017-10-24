from wordcloud import WordCloud
import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import re
import sys
import subprocess

### DataFrame imports for WordCloud###
df = pd.read_csv('WordCloudGenerator_Split/WordCloudPreprocessed.csv',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)
df.columns=['lineId','chId','mId','chName','mName','cleaned_dialogue']
df.head()
df = df[df['cleaned_dialogue'].notnull()]
#########################################

### DataFrame imports for Gender Statistics###
original_movie_title_percentages = pd.read_csv('Gender_Stastics_Visualization/Original_Dialogue_Percentages.csv',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)

imputed_movie_title_percentages = pd.read_csv('Gender_Stastics_Visualization/Imputed_Dialogue_Percentages.csv',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)

# Split genres
def split_genres (genres):
   return (re.sub("[^a-zA-Z-]", " ", genres).split())

movie_titles_split_genres = original_movie_title_percentages
movie_titles_split_genres.geners = original_movie_title_percentages.geners.apply(split_genres)

# To get unique genres in alphabetical order. 
s = movie_titles_split_genres.apply(lambda x: pd.Series(x['geners']),axis=1).stack().reset_index(level=1, drop=True)
list_of_genres = sorted(list(set(s)))

#############################################

def Visualizer():

	
	############################################################
	### Creating a Notebook with different Frames ##############
	############################################################
	
	#Options list for the dropdown
	plt.ion()
	dataset_opt = ['Original','Imputed_Genders']
	list_of_genres.insert(0,'All')
	root = tk.Tk()
	# use width x height + x_offset + y_offset (no spaces!)
	root.geometry("800x400")
	root.title('Visualization Tool')
	# Set resizable FALSE
	#root.resizable(0,0)

	nb = ttk.Notebook(root)
	nb.pack(fill='both', expand='yes')

	# create a child frame for each page
	f1 = tk.Frame(nb)
	f2 = tk.Frame(nb)
	f3 = tk.Frame(nb)
	
	# create the pages
	nb.add(f1, text='WordCloud Generator')
	nb.add(f2, text='Gender_Statistics')
	nb.add(f3, text='Dialogue_Generator')
	
	################################################################
	
	#################################################################
	### Embedding WordCloud Visualization into Frame 1 of Notebook###
	#################################################################
	
	##############################################
	### Functions needed for Word Cloud####
	##############################################
	def getDialogue(name='BIANCA',mName='10 things i hate about you'):
		dialogs = df[(df['chName']==name)&(df['mName']==mName)]['cleaned_dialogue'].values
		if dialogs.shape[0]==0:
			print("Not Found")
			return "Not Found"
		return dialogs

	def getWordCloud(chName,mName):
		dialogues= list(getDialogue(chName,mName))
		words = [word  for dialog in dialogues for word in dialog.split(" ")]
		wordcloud = WordCloud(max_font_size=40,background_color="white").generate(" ".join(words))
		plt.figure()
		plt.title("%s's word cloud from \"%s\""%(chName,mName))
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.axis("off")
		
		plt.show()
		
	def generate_cloud():
		getWordCloud(charselected.get(),movieselected.get())
			
	def generate_characters():        
		char_opt = sorted(list(set(df[(df.mName == movieselected.get())].chName)))
		charselected.set (char_opt[0])
		chardropdown = tk.OptionMenu(f1, charselected, *char_opt)
		chardropdown.place(x=550, y=10)
		
		
	#Options list for the dropdown
	movies_opt = sorted(list(set(df.mName)))
	# Create a variable for the default dropdown option 
	movieselected = tk.StringVar(f1)
	charselected = tk.StringVar(f1)
	# Set the default drop down option 
	movieselected.set('10 things i hate about you')
	charselected.set ('BIANCA')
	# Create the dropdown menu 
	moviedropdown = tk.OptionMenu(f1, movieselected, *movies_opt)
	#char_opt = sorted(list(set(df[(df.mName == movieselected.get())].chName)))
	#chardropdown = OptionMenu(root, charselected, *char_opt)
	# Place the dropdown menu
	moviedropdown.place(x=45, y=10)
	
	#Create a button 
	button11 = tk.Button(f1, text='Please give options for characters', command=generate_characters)
	button11.place(x=300,y=90)

	button12 = tk.Button(f1, text='Generate WordCloud', command=generate_cloud)
	button12.place(x=300,y=190)
	
	
	
	
	#########################################################################
	### Embedding Gender Statistics Visualization into Frame 2 of Notebook###
	#########################################################################
	
	##############################################
	### Functions needed for Gender Statistics####
	##############################################
	def generate_stastics():
		if ((dataset_selected.get())=='Original') :
			df = original_movie_title_percentages
		else: 
			df = imputed_movie_title_percentages
		bins=numpy.linspace(0,100,51)

		if ((genre_selected.get())=='All'):
			fig = plt.figure()
			sub1= fig.add_subplot(211)
			sub1.set_title('%age of Female Dialogues for All Genres for '+dataset_selected.get()+ ' data')
			sub1.set_ylabel('Number of Movies')
			sub1.set_ylim([0,100])
			sub1=plt.hist(df.female_lines_percentage,bins,color='hotpink')
			sub2= fig.add_subplot(212)
			sub2.set_title('%age of Male Dialogues for All Genres for '+dataset_selected.get()+ ' data')
			sub2.set_ylabel('Number of Movies')
			sub2.set_ylim([0,100])
			sub2=plt.hist(df.male_lines_percentage,bins,color='deepskyblue')
			plt.tight_layout()
			plt.show()
		else:
			fig = plt.figure()
			sub1= fig.add_subplot(211)
			sub1.set_title('%age of Female Dialogues for '+genre_selected.get()+' genre for '+dataset_selected.get()+ ' data')
			sub1.set_ylabel('Number of Movies')
			sub1.set_ylim([0,30])
			sub1=plt.hist(df[(df.geners.apply(lambda x: genre_selected.get() in x))].female_lines_percentage,bins,color='hotpink')
			sub2= fig.add_subplot(212)
			sub2.set_title('%age of Male Dialogues for '+genre_selected.get()+' genre for '+dataset_selected.get()+ ' data')
			sub2.set_ylabel('Number of Movies')
			sub2.set_ylim([0,30])
			sub2=plt.hist(df[(df.geners.apply(lambda x: genre_selected.get() in x))].male_lines_percentage,bins,color='deepskyblue')
			plt.tight_layout()
			plt.show()
		   
	def generate_top_10_movies_for_women():
		if ((dataset_selected.get())=='Original'):
			df = original_movie_title_percentages
		else :
			df = imputed_movie_title_percentages
		
		if ((genre_selected.get())=='All'):
			movie_titles_female_percent_top_10=df.sort_values('female_lines_percentage',ascending=True)[-10:].set_index('movieTitle')
		else:
			movie_titles_female_percent_top_10=(df[(df.geners.apply(lambda x: genre_selected.get() in x))]).sort_values('female_lines_percentage',ascending=True)[-10:].set_index('movieTitle')
		#sub3.title('Top 10 Movies with Maximum Percentage of Female Dialogues for'+genre_selected.get()+'genre')
		movie_titles_female_percent_top_10[['female_lines_percentage','male_lines_percentage','unknown_lines_percentage']].plot.barh(stacked=True,color=['hotpink','deepskyblue','grey'],title = 'Top Movies with Max Female Dialogues for '+genre_selected.get()+' genre for '+dataset_selected.get()+ ' data', legend=False)
		plt.show()
		
	def generate_top_10_movies_for_men():
		if ((dataset_selected.get())=='Original'):
			df = original_movie_title_percentages
		else :
			df = imputed_movie_title_percentages
		
		if ((genre_selected.get())=='All'):
			movie_titles_male_percent_top_10=df.sort_values('male_lines_percentage',ascending=True)[-10:].set_index('movieTitle')
		else:
			movie_titles_male_percent_top_10=(df[(df.geners.apply(lambda x: genre_selected.get() in x))]).sort_values('male_lines_percentage',ascending=True)[-10:].set_index('movieTitle')
		movie_titles_male_percent_top_10[['female_lines_percentage','male_lines_percentage','unknown_lines_percentage']].plot.barh(stacked=True,color=['hotpink','deepskyblue','grey'],title = 'Top Movies with Max Male Dialogues for '+genre_selected.get()+' genre for '+dataset_selected.get()+ ' data',legend=False)
		plt.show()
		
		
	# Create a variable for the default dropdown option 
	dataset_selected = tk.StringVar(f2)
	genre_selected = tk.StringVar(f2)
	# Set the default drop down option 
	dataset_selected.set('Original')
	genre_selected.set ('All')
	# Create the dropdown menu 
	dataset_dropdown = tk.OptionMenu(f2, dataset_selected, *dataset_opt)	
	genre_dropdown = tk.OptionMenu(f2, genre_selected, *list_of_genres)
	# Place the dropdown menu
	dataset_dropdown.place(x=45, y=10)
	genre_dropdown.place(x=550, y=10)
	

	#Create a button 
	button21 = tk.Button(f2, text='Generate stastics for percentage of dialogues for women/men', command=generate_stastics)
	button21.place(x=200,y=90)

	button22 = tk.Button(f2, text='Generate top 10 movies with maximum dialogues for women', command=generate_top_10_movies_for_women)
	button22.place(x=200,y=190)
	
	button23 = tk.Button(f2, text='Generate top 10 movies with maximum dialogues for men', command=generate_top_10_movies_for_men)
	button23.place(x=200,y=290)
	
	#########################################################################
	### Embedding Dialogue Generator into Frame 3 of Notebook###
	#########################################################################
	def dialogue_generator():
		result = subprocess.check_output([
		sys.executable, 
		'../dialog_generator/char_rnn_tensorflow_master/sample.py',
		'--save_dir=../dialog_generator/char_rnn_tensorflow_master/save/' + genreselected.get() + '_' + ratingselected.get()
		]).decode().replace('\\r\\n', '\n').replace('\\t', '\t').replace('b', '').replace('"', '').strip()
		print(result)
		
	genre_opt = ['action','comedy','drama']
	rating_opt = ['low','mid','high']
	genreselected = tk.StringVar(f3)
	ratingselected = tk.StringVar(f3)
	# Set the default drop down option 
	genreselected.set('action')
	ratingselected.set ('low')
	# Create the dropdown menu 
	genredropdown = tk.OptionMenu(f3, genreselected, *genre_opt)
	ratingdropdown = tk.OptionMenu(f3, ratingselected, *rating_opt)
	# Place the dropdown menu
	genredropdown.place(x=45, y=10)
	ratingdropdown.place(x=550, y=10)
	
	#Create a button 
	button31 = tk.Button(f3, text='Generate Dialogues', command=dialogue_generator)
	button31.place(x=300,y=90)
	
	
	root.mainloop()
	
Visualizer()
plt.close('all')
plt.ioff()