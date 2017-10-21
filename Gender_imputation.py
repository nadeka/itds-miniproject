
import pandas as pd
character_df=pd.read_csv('CleanUp/movie_characters_metadata_cleanup.tsv',sep='\t',header=0, error_bad_lines=False, warn_bad_lines=False)
print character_df.head()
print character_df.shape###(9032, 5)
###covert gender column values into lower case
character_df.gender = character_df.gender.str.lower()
character_df.characterName = character_df.characterName.str.upper()
###count of character on gender  
print character_df.gender.value_counts()
# ?    6017
# m    2049
# f     966

####Step 1: determine character gender based on name_gender.csv
name_gender = pd.read_csv('name_gender.csv')
# print name_gender.shape###(95026, 3)
####captialize the name and also lowercase the gender
name_gender.name = name_gender.name.str.upper()	
name_gender.gender = name_gender.gender.str.lower()
###Change the name_gender column name to characterName to later merge
name_gender = name_gender.rename(columns = {'name':'characterName'})
print name_gender.head()
df1 = character_df[character_df['gender']=='?']

#### Merge the name_gender and df1 with characterName to determine gender for the characterName
df_merge = pd.merge(df1, name_gender, how='inner', on=['characterName'],left_index=False, right_index=False, sort=True,
		 suffixes=('_x', '_y'), copy=True, indicator=False)
print df_merge.head()
print df_merge.shape###(2998, 7)
###Get name_gender dictionary
name_gender_dict = dict(zip(df_merge.characterName,df_merge.gender_y))
name_list = list(name_gender_dict.keys())
for index, row in character_df.iterrows():
     if row.characterName in name_list:
         row.gender = name_gender_dict.get(row.characterName)
print character_df.gender.value_counts()
# m    4087
# ?    3019
# f    1926
####After using the name_gender.csv to determine gender, gender counts are below:
print character_df.head()

####Step 2: determine gender of character based on hint such as Miss, MRS etc
hint1_female_on_name = ['GIRL', 'MOTHER', 'MISS', 'WAITRESS', 'WIFE', 'SISTER', 'GRANDMA', 'GRANDMOTHER', 'QUEEN', 'PRINCESS', 'MAID']
hint2_female_on_name = ["'S WIFE", "'S SISTER", "'S MOTHER", "'S MOM", "MISS ", "MRS. ", "MRS ", "MADAM ", "MADAME ", " QUEEN", "PRINCESS ", " PRINCESS"]
hint1_male_on_name = ["MAN", "FATHER", "BOY", "GRANDAD", 'BROTHER', "GRANDFATHER", "GRANDPA", "BOYFRIEND", "GRANDSON", "DUKE", "KING", "PRINCE"]
hint2_male_on_name = ["'S FATHER", "'S SON", "'S DAD", "MR. ", "MR ", "SIR ", "DUKE ", " DUKE", " KING", "KING ", "PRINCE ", " PRINCE", "MASTER "]
for index, row in character_df.iterrows():
    if row.characterName in hint1_female_on_name:
        row.gender='f'
    elif row.characterName in hint1_male_on_name:
        row.gender='m'
###characterName contains gender related info  
for index, row in character_df.iterrows():
    for j in hint2_male_on_name:
        if j in row.characterName:
            row.gender='m'
    for i in hint2_female_on_name:
        if i in row.characterName:
            row.gender='f'
print character_df.gender.value_counts() 
# m    4191
# ?    2734
# f    2107

###Step 3: determine gender based on characterName whose gender is determined, since there are some names could be both male and female, those names are excluded for determination
male_characters = character_df[character_df['gender']=='m']
female_characters = character_df[character_df['gender']=='f']
unknow_gender_character = character_df[character_df['gender']=='?']
male_names = male_characters.characterName.unique()
female_names=female_characters.characterName.unique()
unknow_names = unknow_gender_character.characterName.unique()
def getCommonElements(list1, list2):
	return list(set(list1)&set(list2))

def getUncommonElements(list1, list2):
	return list(set(list1)-set(list2))
common_names = getCommonElements(male_names, female_names)
print common_names 
print len(common_names)#
uknow_male_common = getCommonElements(male_names, unknow_names)
unknow_female_common = getCommonElements(female_names, unknow_names)
name_could_be_male_female = getCommonElements(unknow_names, common_names)
malenames_exclude_common = getUncommonElements(male_names, common_names)
female_names_exclude_common = getUncommonElements(female_names, common_names)

for index, row in character_df.iterrows():
    for m in malenames_exclude_common:
        if row.characterName==m:
            row.gender='m'
    for f in female_names_exclude_common:
        if row.characterName==f:
            row.gender='f'
print character_df.gender.value_counts()
# m    4369
# ?    2494
# f    2169

character_df.to_csv('CleanUp/movie_characters_metadata_cleanup_gender.csv', sep='\t', index=False, header=None)

