#This file is to move pdfs of german docs to txt files

#Importing the required packages
import os
import pandas as pd
import glob
from collections import Counter
import regex as re
import sys
import PyPDF2
from pdfminer.high_level import extract_text 
import textract
from tqdm import tqdm
# listing all folders in the directory "Files/DE Text to Analyse/DIP Lists/"
folders = os.listdir('../Files/German/Pull No 3 for 2 Word Items/DIP Lists/')

try:
    folders.pop(folders.index('.DS_Store')) # this is a specific MacOS file that may or may not exist, but don't want it
except ValueError:
    pass

for folder in folders:
    path = os.path.join('../Files/German/Pull No 3 for 2 Word Items/DIP Lists/' + folder)
    isExist = os.path.exists(path)

    if not isExist:
        print(path) # Create a new directory because it does not exist
        
# Within each folder, there are .pdf files that we want
files = []
for folder in folders: 
    temp = os.listdir(os.path.join('../Files/German/Pull No 3 for 2 Word Items/DIP Lists/' + folder)) 
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
#How to Get Raw Text
def pdftotxt(file):
    text = textract.process(os.path.join('../Files/German/Pull No 3 for 2 Word Items/DIP Lists/' +  file), method='pdfminer')
    text = text.decode('utf-8') # since textract gives us unicode, we decode it to utf-8 encoding to use it as str
    with open(os.path.join('../Files/German/Pull No 3 for 2 Word Items/DIP Lists/' + file[:-4] + '.txt'), 'w') as newtext:
        newtext.write(text)  # we save the file as a text file in the same folder
for file in tqdm(files): # convert all pdf to txt files
    pdftotxt(file)