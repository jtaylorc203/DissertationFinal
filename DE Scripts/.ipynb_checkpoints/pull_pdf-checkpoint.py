import requests
import os
import textract
from tqdm import tqdm
import pandas as pd
# listing all folders in the directory "Files/DE"
folders = os.listdir('../Files/German/Text Analysis/Final CSVs/')

try:
    folders.pop(folders.index('.DS_Store')) # this is a specific MacOS file that may or may not exist, but don't want it
except ValueError:
    pass

for folder in folders:
    path = os.path.join('../Files/German/Text Analysis/Final CSVs/' + folder)
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path) # Create a new directory because it does not exist
        
folders
# Within each folder, there are .pdf files that we want
files = []
for folder in folders: 
    temp = os.listdir(os.path.join('../Files/German/Text Analysis/Final CSVs/' + folder)) 
    try:
        temp.pop(temp.index('.ipynb_checkpoints'))
    except ValueError:
        pass
    try: 
         temp.pop(temp.index('.DS_Store')) # our subfolders may also contain the .DS_Store file, so we try to remove as well
    except ValueError:
        pass
    for t in temp:
        files.append(os.path.join('../Files/German/Text Analysis/Final CSVs/' + folder + '/' + t)) # we save our file names directly as the entire path
        
def get_pdf(url):
    """_
    Get the pdf from the url
    """
    pdf = requests.get(url, stream=True)
    return pdf

def save_pdf(pdf):
    """
    Save the pdf to file
    """
    with open(os.path.join('../Files/German/Text Analysis/Activity_texts/temp.pdf'), 'wb') as f:
        f.write(pdf.content)
    f.close()

def pdftotxt(file):
    text = textract.process(file, method='pdfminer')
    text = text.decode('utf-8') # since textract gives us unicode, we decode it to utf-8 encoding to use it as str
    filename = text.split('\n')[0].replace('/','\\')
    with open(os.path.join('../Files/German/Text Analysis/Activity_texts/' + filename + '.txt'), 'w') as newtext:
        newtext.write(text)  # we save the file as a text file in the same folder
    os.remove(file)
    return filename

def download_pdf(url):
    """
    Download the pdf from the url and save it to file
    """
    pdf = get_pdf(url)
    save_pdf(pdf)
    filename = pdftotxt('../Files/German/Text Analysis/Activity_texts/temp.pdf')
    print(f"Downloaded: {filename}")



if __name__ == '__main__':
    df = pd.read_csv('../Files/German/Text Analysis/Final CSVs/Uncounted/' + t)
    urls = df.URLs.to_list()
    for url in tqdm(urls):
        download_pdf(url)