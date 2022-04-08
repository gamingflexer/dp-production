import spacy
from tika import parser
import numpy as np
import torch
from keras.preprocessing.sequence import pad_sequences
from transformers import BertForTokenClassification, BertTokenizerFast
import torch
from keras.preprocessing.sequence import pad_sequences
from pytorch_pretrained_bert import BertForTokenClassification, BertAdam, BertTokenizer, BertConfig
from keras.preprocessing.text import Tokenizer
import torch.nn.functional as F
import torch.nn as nn
import textract
from tika import parser
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
import pyperclip
import re
from autocorrect import Speller
from simplet5 import SimpleT5
from constants import *
from config import spacy_700_path
from preprocessing import remove_hexcode_rhc, summary_clean
from fileconversion import fileconversion0000
from parser2 import resumeparse
from parser1 import mainML
from parser1 import *
from parser2 import *
from preprocessing import dict_clean, summary_clean

spell = Speller(fast=True, lang='en')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

def parser(fname):
    p4 =[]
    to_delete = ['email', 'phone', 'name', 'total_exp',
                 'designition','FileName','skills', 'File Language']  # 2
    p1 = mainML.get_parsed(fname)
    p2 = resumeparse.read_file(fname)
    # p3 = spacy_700(fname)
    # print(f'P3-testing ---- {p3}')

    p1.update(p2)
    for i in to_delete:
        try:
            del p1[i]
        except:
            continue
    #skills merge
    # p4 = p1['Skills'] + p1['skills']
    # p1.pop('Skills')
    # p1.pop('skills')
    
    #remove bad words in skills
    # try:
    #   for bad in BAD_words:
    #       p4.remove(bad)
    # except:
    #   pass

        
    # p1.update({"Skills":p4})
    p2 = dict_clean(p1)
    return p2

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def spacy_700(path):
    text = fileconversion1(path,y=0)
    o1 = {}
    spacy_700_list = []
    model_spacy_path_all = spacy_700_path

    model_spacy = spacy.load(model_spacy_path_all)

    # predict
    doc = model_spacy(text)
    for ent in doc.ents:
        if ent.label_.upper() in tagvalues_spacy:
            temp = {f'{ent.label_.upper():{4}}': [ent.text]}
            spacy_700_list = spacy_700_list + [temp]
    for val in spacy_700_list:
        o1.update(val)
    #del model_spacy
    return o1

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def summary(text, model_summary):
    # add pre-processed text (no hex one)
    text_to_summarize = f"""summarize:{text}"""
    summary = model_summary.predict(text_to_summarize)
    summary_1 = summary[0]
    summary_1 = remove_hexcode_rhc(summary_1)
    summary_2 = spell(summary_1)
    summary_2 = summary_clean(summary_2)
    return summary_2

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def summary_extractive(text):
    outputs = learn.blurr_generate(text, early_stopping=False, num_return_sequences=1)
    return outputs

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


#spacy - skills

# def spacy_skills(text):
#     o2 = {}
#     spacy_skills_list = []
#     model_skills = spacy_skills_path

#     model_spacy_s = spacy.load(model_skills)

#     # predict
#     doc = model_spacy_s(text)
#     for ent in doc.ents:
#         if ent.label_.upper() in tagvalues_spacy:
#             temp = {f'{ent.label_.upper():{4}}': [ent.text]}
#             spacy_skills_list = spacy_skills_list + [temp]
#     for val in spacy_skills_list:
#         o2.update(val)
#     return (o2)

# #spacy - Edu

# def spacy_edu(text):
#     o3 = {}
#     spacy_edu_list = []
#     model_edu = spacy_edu_path

#     model_spacy_e = spacy.load(model_edu)

#     # predict
#     doc = model_spacy_e(text)
#     for ent in doc.ents:
#         if ent.label_.upper() in tagvalues_spacy:
#             temp = {f'{ent.label_.upper():{4}}': [ent.text]}
#             spacy_edu_list = spacy_edu_list + [temp]
#     for val in spacy_edu_list:
#         o3.update(val)
    return (o3)

#spacy - Exp

# def spacy_exp(text):
#     o4 = {}
#     spacy_exp_list = []
#     model_exp = spacy_exp_path

#     model_spacy_exp = spacy.load(model_exp)

#     # predict
#     doc = model_spacy_exp(text)
#     for ent in doc.ents:
#         if ent.label_.upper() in tagvalues_spacy:
#             temp = {f'{ent.label_.upper():{4}}': [ent.text]}
#             spacy_exp_list = spacy_exp_list + [temp]
#     for val in spacy_exp_list:
#         o4.update(val)
#     return (o4)


# Compare

def comparemain(text):

    classifier = pipeline("zero-shot-classification")
    # classes to divide into or not
    candidate_labels = ['Skills', 'Degree',
                        'Companies worked at', 'Name', 'Rewards and Achievements']
    output = classifier(text, candidate_labels, multi_class=False)

    # last element of the dict
    final_list = {output['sequence']: output['labels'][0]}
    print(output['scores'][0])
    return final_list


# NER

def ner(text, model, tokenizer):
    # create a pipleine to get the output
    nlp = pipeline('ner', model=model, tokenizer=tokenizer)
    ner_list = nlp(text)

    # Person Name
    this_name = []
    all_names_list_tmp = []

    for ner_dict in ner_list:
        if ner_dict['entity'] == 'B-PER':
            if len(this_name) == 0:
                this_name.append(ner_dict['word'])
            else:
                all_names_list_tmp.append([this_name])
                this_name = []
                this_name.append(ner_dict['word'])
        elif ner_dict['entity'] == 'I-PER':
            this_name.append(ner_dict['word'])

    all_names_list_tmp.append([this_name])

    final_name_list = []
    for name_list in all_names_list_tmp:
        full_name = ' '.join(name_list[0]).replace(
            ' ##', '').replace(' .', '.')
        final_name_list.append([full_name])

    if (len(final_name_list)) > 1:
        final_name_list2 = str(final_name_list[0]) + str(final_name_list[1])
        final_name_list2 = final_name_list2.replace("]", "")
        final_name_list2 = final_name_list2.replace("[", "")
        final_name_list2 = final_name_list2.replace("'", "")
        final_name_list2 = final_name_list2.replace("]", "")

    return final_name_list

    # clean spacy
    # if same in any dict delete
    # keyword - not possible in spacy
    # after , remove for name

    # main = []
    # for i in entities1:
    #     if i['entity'] in tags_vals:
    #         k = {i['entity']: i['text']}
    #         main = main + [k]

    # #save & clean
    # k = len(main)

    # # clean unnescaary values
    # r = []
    # for k in range(len(main)):
    #     for key, value in main[k].items():
    #         # print(value)
    #         if value == '':
    #             r = r + [k]
    #             # main.remove(main[k])
    #         elif value == ':':
    #             r = r + [k]
    #         elif value == ',':
    #             r = r + [k]
    #         elif value == 'Resume':
    #             r = r + [k]
    #         elif value == '.':
    #             r = r + [k]
    #         elif value == ' ':
    #             r = r + [k]
    #         elif value == '.':
    #             r = r + [k]
    #         elif value == '.':
    #             r = r + [k]

    # for rr in range(len(r)):
    #     main.remove(main[rr])
    # r.clear()

    # # clean unnesacry keys
    # for val in main:
    #     for key, value in val.items():
    #         if key == "Email Address":
    #             main.remove(val)
    #         elif key == "UNKNOWN":
    #             main.remove(val)
    #         elif key == "Empty":
    #             main.remove(val)

    # print(main)
