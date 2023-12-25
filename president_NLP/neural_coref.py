'''
This is a file that i ran locally on terminal instead of in jypter notebook, to run this code you want to do this in a conda environment with python, scpacey 2.1.1 and also have neuralcoref installed in that environment.
'''

import spacy
import neuralcoref
import pandas as pd

file=pd.read_csv("outputfinal_filename.csv")

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

overall = pd.DataFrame(columns=['doc_name', 'date', 'transcript', 'president', 'title', 'Year'])

for i in range(len(file)):
    prez=str(file.loc[i, "president"])
    trans=str(file.loc[i, "transcript"])
    prez= prez.replace(" ", "")
    final= trans.replace('I ',""+prez+" " )
    doc=nlp(final)
    resolved_text = doc._.coref_resolved
    
    overall.loc[i, 'doc_name']= file.loc[i, "doc_name"]
    overall.loc[i, 'date']= file.loc[i, "date"]
    overall.loc[i, 'transcript']= resolved_text
    overall.loc[i, 'president']= file.loc[i, "president"]
    overall.loc[i, 'title']= file.loc[i, "title"]
    overall.loc[i, 'Year']= file.loc[i, "Year"]
    
    print(""+str(i)+"/"+str(len(file))+"")
    
    
    
    
overall.reset_index(inplace=True)
overall.drop('index', axis=1, inplace=True)   
overall.to_csv('neuraled.csv', index=False)   