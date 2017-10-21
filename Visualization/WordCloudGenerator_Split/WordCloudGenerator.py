from wordcloud import WordCloud
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
#Let's create a function to create a word cloud out of one character
#Get only lines spoken by out focus characters

df = pd.read_csv('WordCloudPreprocessed.csv',encoding='ISO-8859-2',error_bad_lines=False,warn_bad_lines =False,header=0)
df.columns=['lineId','chId','mId','chName','dialogue','mName','gender','cleaned_dialogue']
df.head()
df = df[df['dialogue'].notnull()]
df = df[df['cleaned_dialogue'].notnull()]

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

def randomWordCloud():
	sample = df.sample(1)
	getWordCloud(sample['chName'].values[0],sample['mName'].values[0])

def WordCloudGenerator():
	# Create functions for conversion
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
		chardropdown = OptionMenu(root, charselected, *char_opt)
		chardropdown.place(x=550, y=10)
		

	#Options list for the dropdown
	movies_opt = sorted(list(set(df.mName)))
	#char_opt = ['BIANCA','PETE','WADE']
	# Create the main window 
	root = Tk()
	# Rename the title of the window    
	root.title("WordCloud Generator")
	# Set the size of the window
	root.geometry("800x250")
	# Set resizable FALSE
	root.resizable(0,0)
	# Create a variable for the default dropdown option 
	movieselected = StringVar(root)
	charselected = StringVar(root)
	# Set the default drop down option 
	movieselected.set('10 things i hate about you')
	charselected.set ('BIANCA')
	# Create the dropdown menu 
	moviedropdown = OptionMenu(root, movieselected, *movies_opt)
	#char_opt = sorted(list(set(df[(df.mName == movieselected.get())].chName)))
	#chardropdown = OptionMenu(root, charselected, *char_opt)
	# Place the dropdown menu
	moviedropdown.place(x=45, y=10)
	

	

	#Create a button 
	button1 = Button(root, text='Please give options for characters', command=generate_characters)
	button1.place(x=300,y=90)

	button2 = Button(root, text='Generate WordCloud', command=generate_cloud)
	button2.place(x=300,y=190)

	root.mainloop()

WordCloudGenerator()
