"""
Pulling txt files from the US congress website and saving them as txt file
"""

# Importing the required packages
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import sys
sys.setrecursionlimit(50000)

# listing all folders in the directory "Files/US"
folders = os.listdir('../Files/US/')

try:
    folders.pop(folders.index('.DS_Store')) # this is a specific MacOS file that may or may not exist, but don't want it
except ValueError:
    pass
folders.pop(folders.index('Executive')) # for the Executive branch, we only have a pdf document, which we will deal with somewhere else
folders.pop(folders.index('Text_pulled')) # for the Executive branch, we only have a pdf document, which we will deal with somewhere else

# Within each folder, there are .csv files that we want
files = []
for folder in folders: 
    temp = os.listdir(os.path.join('../Files/US/' + folder)) 
    try:
        temp.pop(temp.index('.ipynb_checkpoints'))
    except ValueError:
        pass
    try: 
         temp.pop(temp.index('.DS_Store')) # our subfolders may also contain the .DS_Store file, so we try to remove as well
    except ValueError:
        pass
    for t in temp:
        files.append(os.path.join('../Files/US/' + folder + '/' + t)) # we save our file names directly as the entire path

for file in files: # we run through the files
    print(file)
    df = pd.read_csv(file, header=2) # read in the files
    for i, j in df.iterrows(): # and then pull the text from each URL we have found
        url = j.URL
        record_type = file.split('/')[-1][-10:-4]
        print(file.split('/')[-1][:-4]+ df.iloc[i][0].split(';')[-1], "url ", url)
        
        
        if record_type == 'lation': # If our text is a legislation document 
            url = url + '/text?format=txt'
            req = requests.get(url) # retrieve HTML content from the URL
            soup = BeautifulSoup(req.content, 'html.parser') # parse contents
            try:
                text = soup.find(id='billTextContainer') # find full text in web page
                text = str(text.contents[1])
            except (AttributeError, IndexError) as e:
                print('Error, did not pull for', e)
                pass
        
        elif record_type == 'Report' or record_type == 'eports': # If our text is a report 
            req = requests.get(url) # retrieve HTML content from the URL
            soup = BeautifulSoup(req.content, 'html.parser') # parse contents
            try:
                text = soup.find(id='report') # find full text in web page
                text = str(text.contents[3])
            except (AttributeError, IndexError) as e:
                print('Error, did not pull for', e)
                pass
        
        else: # Else is for Congressional Records and Remarks
            req = requests.get(url) # retrieve HTML content from the URL
            soup = BeautifulSoup(req.content, 'html.parser') # parse contents
            try:
                text = soup.find(id='content') # find full text in web page
                text = str(text.contents[5])
            except (AttributeError, IndexError):
                print('Error, did not pull')
                pass
        
        
        if type(text) == str:
            with open(os.path.join (  '../Files/US/Text_pulled/' + file.split('/')[-1][:-4]+ df.iloc[i][0].split(';')[-1] + '.txt'), 'w') as text_file: 
                    text_file.write(str(text)) # we save the file as a text file

