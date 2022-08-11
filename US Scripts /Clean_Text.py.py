#This file is to clean text for the text analysis

#Importing the required packages
import os
import regex as re

# listing all folders in the directory "Files/US"
folders = os.listdir('../Files/US/Text_pulled/')

try:
    folders.pop(folders.index('.DS_Store')) # this is a specific MacOS file that may or may not exist, but don't want it
except ValueError:
    pass

for folder in folders:
    path = os.path.join('../Files/US/Text_cleaned/'+ folder)
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path) # Create a new directory because it does not exist

# Within each folder, there are .csv files that we want
files = []
for folder in folders: 
    temp = os.listdir(os.path.join('../Files/US/Text_pulled/' + folder)) 
    try:
        temp.pop(temp.index('.ipynb_checkpoints'))
    except ValueError:
        pass
    try: 
         temp.pop(temp.index('.DS_Store')) # our subfolders may also contain the .DS_Store file, so we try to remove as well
    except ValueError:
        pass
    for t in temp:
        files.append(os.path.join(folder + '/' + t)) # we save our file names directly as the entire path



#How to Clean Text
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext




for file in files:
    with open(os.path.join('../Files/US/Text_pulled/' + file), 'r') as text:
        txt = text.read()
    
    clean_txt = cleanhtml(txt)

    with open(os.path.join('../Files/US/Text_cleaned/' + file), 'w') as clntext:
        clntext.write(clean_txt)  # we save the file as a text file
    print(f'cleaned & saved file {file}')