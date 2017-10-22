from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy


original_movie_title_percentages = pd.read_csv('Original_Dialogue_Percentages.csv',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)

imputed_movie_title_percentages = pd.read_csv('Imputed_Dialogue_Percentages.csv',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)

# Split genres
def split_genres (genres):
   return (re.sub("[^a-zA-Z-]", " ", genres).split())

movie_titles_split_genres = original_movie_title_percentages
movie_titles_split_genres.geners = original_movie_title_percentages.geners.apply(split_genres)

# To get unique genres in alphabetical order. 
s = movie_titles_split_genres.apply(lambda x: pd.Series(x['geners']),axis=1).stack().reset_index(level=1, drop=True)
list_of_genres = sorted(list(set(s)))

def Gender_Stastics_Visualizer():

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
		
	#Options list for the dropdown
	plt.ion()
	dataset_opt = ['Original','Imputed_Genders']
	list_of_genres.insert(0,'All') 	
	# Create the main window 
	root = Tk()
	# Rename the title of the window    
	root.title("Gender Dialogue Stastics")
	# Set the size of the window
	root.geometry("800x350")
	# Set resizable FALSE
	root.resizable(0,0)
	# Create a variable for the default dropdown option 
	dataset_selected = StringVar(root)
	genre_selected = StringVar(root)
	# Set the default drop down option 
	dataset_selected.set('Original')
	genre_selected.set ('All')
	# Create the dropdown menu 
	dataset_dropdown = OptionMenu(root, dataset_selected, *dataset_opt)	
	genre_dropdown = OptionMenu(root, genre_selected, *list_of_genres)
	# Place the dropdown menu
	dataset_dropdown.place(x=45, y=10)
	genre_dropdown.place(x=550, y=10)
	

	#Create a button 
	button1 = Button(root, text='Generate stastics for percentage of dialogues for women/men', command=generate_stastics)
	button1.place(x=200,y=90)

	button2 = Button(root, text='Generate top 10 movies with maximum dialogues for women', command=generate_top_10_movies_for_women)
	button2.place(x=200,y=190)
	
	button3 = Button(root, text='Generate top 10 movies with maximum dialogues for men', command=generate_top_10_movies_for_men)
	button3.place(x=200,y=290)

	root.mainloop()
	
Gender_Stastics_Visualizer()
plt.close('all')
plt.ioff()