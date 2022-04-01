import re
import nltk
from nltk import ngrams
import os
import spacy
import config

# Removing Ansi from text
def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


############################### CLEANING DATA ###########################
def get_new_data(text):
    new_data = ''
    req = [lines for  lines in text.split('\n')]
    for r in req:
        if ('reference' in r.lower() or 'references' in r.lower()  or 'referee' in r.lower() or 'referees' in r.lower()) and len(r.split()) < 4:
            break
        new_data += r + '\n'
    return new_data


def preprocess_text(new_text):
    req = ''
    for line in new_text.split('\n'):
        ll = re.sub(r'[^0-9a-zA-Z]+', ' ',line)
        req += ll + '\n'
        new_text = req
    return new_text


def extract_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [ ' '.join(grams) for grams in n_grams]

def remove(string): 
    pattern = re.compile(r'\s+') 
    return re.sub(pattern, '', string)


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

################################ CUSTOM ENTITIES ###################

def get_custom_entities(text):
    
    model_dir = config.resume_model

    nlp2 = spacy.load(model_dir)
    doc2 = nlp2(text)
    entities = extract_entities(doc2)
    for key, val in entities.items():
        entities[key] = clean_text(val)            
    return entities

def clean_text(val):
    result = list()
    for each in val:
        out = re.sub(r'[^0-9a-zA-Z]+', ' ', each)   
        result.append(out)      
    return result


### Custom Entities:
def extract_entities(custom_nlp_text):
    entities = {}
    for ent in custom_nlp_text.ents:
        if ent.label_ not in entities.keys():
            entities[ent.label_] = [ent.text]
        else:
            entities[ent.label_].append(ent.text)
    for key in entities.keys():
        entities[key] = list(set(entities[key]))
    return entities

def tokenize_text(text):
    lines = [each for each in text.split('\n') if len(each)>0]
    lines = [nltk.word_tokenize(each) for each in lines]
    lines = [nltk.pos_tag(each) for each in lines]

    return lines

