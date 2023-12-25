'''
This is a file that i ran locally on terminal instead of in jypter notebook, to run this code you want to do this in a conda environment with python, scpacey 2.1.1.
'''

import spacy
import pandas as pd
from textblob import TextBlob

file=pd.read_csv("neuraled.csv")
# Load spaCy model
nlp = spacy.load('en_core_web_sm')
relations = pd.DataFrame(columns=['entity1','entity2',  'sentiment',  'date',  'president', 'title', 'Year'])

for e in range(int(len(file))):
    
    text = file.loc[e, 'transcript' ]
    print(""+str(e)+"/"+str(int(len(file)))+"")

    # Process the text
    doc = nlp(text)

    # Assuming we are interested in relations involving two proper nouns (entities)
    entities = [ent for ent in doc if ent.pos_ == 'PROPN']

    
    ## precations to make sure two word entites are not being analysied seperately
    p=0
    # Extracting relationships and performing sentiment analysis
    for i in range(len(entities)-1):
        entity1 = entities[i]

        # Example: Checking if entities appear in the same sentence
        combined_entities = str(entity1) + ' ' + str(entities[i+1])
                                                     
        if p>0:
            p=p-1
            continue
        k=0
        if combined_entities in entity1.sent.text:
            entity1= combined_entities
            k=k+1
        for j in range(i+1, len(entities)):
            entity2 = entities[j]

            if k==1:
                k=k-1
                p=p+1
                continue

            if (j < len(entities)-2):
                # Example: Checking if entities appear in the same sentence
                combined_entities = str(entity2) + ' ' + str(entities[j+1])

            if combined_entities in entity2.sent.text:
                entity2= combined_entities





            # Example: Checking if entities appear in the same sentence

            if entities[i].sent == entities[j].sent :
                # Sentiment analysis on the sentence
                sentiment = TextBlob(str(entities[i].sent)).sentiment
                
                
                rel = pd.DataFrame({
                    'entity1': [entity1],
                    'entity2': [entity2],

                    'sentiment': [sentiment.polarity], # Polarity score: -1 (negative) to 1 (positive)
     
                    'date': [file.loc[e, 'date']],
    
                    'president': [file.loc[e, 'president']],
                    'title': [file.loc[e, 'title']],
                    'Year': [file.loc[e, 'Year']]
                })
                relations=pd.concat([relations,rel],ignore_index=True) 
                
  
                
                
                
                
relations.reset_index(inplace=True)
relations.drop('index', axis=1, inplace=True)   
relations.to_csv('relationships1.csv', index=False) 