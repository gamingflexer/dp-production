import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd
import re
from models import constants as com
import os
import string
import nltk
from nltk.corpus import stopwords
import pickle
import csv
import json
import numpy as np
from fuzzywuzzy import fuzz
import phonenumbers 
from models import constants as comm
import config
import preprocessing as utils
from model import ner
en_sm = spacy.load('en_core_web_sm')


nlp = config.en_sm
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True )



def get_total_years(text):
    for line in text.split('\n'):
        if 'experience' in  line.lower() and 'years' in line.lower():
            sen_tokenised= nltk.word_tokenize(line)
            tagged = nltk.pos_tag(sen_tokenised)
            entities = nltk.chunk.ne_chunk(tagged)
            for subtree in entities.subtrees():
                for leaf in subtree.leaves():
                    if leaf[1]=='CD':
                        experience_years = leaf[0]  
                        return experience_years
    return ''

# Function for obtaining language
def get_lang(text):
    text = nlp(text)
    language = text._.language["language"]
    if language == 'en':
        language = 'English'
    return language

################################# GET extras Categories   ###############
def get_extra(text, category):
    try:
        count = 0
        ents = get_head_sections(text)
        _string = ''
        req = ents[category]
        for each in req.split('\n'):
            if len(each.split()) < 2:
                continue
            select = each.split('.')
            try:
                each = select[0] + '.' + select[1]
            except:
                each = select[0] 
            _string += utils.preprocess_text(each) 
            count += 1      
            if count > 12:break
            if len(_string.split()) > 200:break  
        return _string
    except:pass
    return ''


####################### Skills ###########################################

def get_custom_skills(text):
    skill_set = list()
    try:
        with open(config.skill_rb, 'rb') as fp:
            skills = pickle.load(fp)
        for skill in skills:
            # print(skill)
            skill = ' '+skill+' '
            if skill.lower() in text:
                skill_set.append(skill)
        return skill_set
    except:
        skill_set


def get_skills(custom_entities, text):

    exp = get_head_sections(text)['skills']
    try:
        model_dir = config.skill_model_dir
        nlp2 = spacy.load(model_dir) ###########################################
        doc2 = nlp2(exp)
        entities = utils.extract_entities(doc2)
        for key, val in entities.items():
            entities[key] = utils.clean_text(val)            
        if len(entities['Skills']) > 4:
            return entities['Skills']
    except:
        print("No skills entitiy")
        
    skills = list()
    exp = []
    lines = [lin.strip() for lin in text.split('\n')]            

    for ind, line in enumerate(lines):
        if len(line.split()) < 4 and ('skills' in line.lower()) :
            try:
                for i in range(1,5):
                    exp.append(lines[ind+i])   
            except:
                exp.append(lines[ind+i])  
    description = [e for e in exp if not e[:5].lower() =='level' and len(e)>0]
    exp = get_head_sections(text)['skills']
    if len(exp.split('\n')) < 4:
        exp = ''
        for ind, line in enumerate(lines):
            if len(line.split()) < 8 and ('skills' in line.lower()  or 'expertise' in line.lower()  or 'strength' in line.lower() or 'proficiency' in line.lower() ) :
                try:
                    try:
                        try:
                            for i in range(1,25):
                                exp += lines[ind+i] + ' '
                        except:
                            for i in range(1,15):
                                exp += lines[ind+i] + ' ' 
                    except:
                        for i in range(1,10):
                            exp += lines[ind+i] + ' ' 
                except:
                    exp += lines[ind+1] + ' ' + lines[ind+2]    
                
    exp = exp.lower()
    skillset = list()
    skill_dict = {}
    nlp_text = nlp(exp)
    noun_chunks = list(nlp_text.noun_chunks)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(config.skill_csv)

    bigrams = utils.extract_ngrams(exp,2) 

    skills = list(data.columns.values)
    custom_skillset =  get_custom_skills(text)
    try:

        # check for one-grams
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)

        # check for bi-grams and tri-grams
        for token in noun_chunks:
            token = token.text.lower().strip()
            if token in skills and token not in skillset:
                skillset.append(token)
        for token in bigrams:
            if token.lower() in skills and token not in skillset:
                skillset.append(token)
        skillset = [i.lower() for i in set([i.lower() for i in skillset])]
        if len(skillset) < 5:
            for skill in custom_skillset:
                if skill not in skillset:
                    skillset.append(skill)
            try:     
                skillset = skillset[:5]
            except:
                pass       
        skillset = [i.capitalize() for i in set([i.lower() for i in skillset])]
        skillset = [i.strip() for i in skillset if not i in (' a ') ]
        skillset = sorted(skillset, key = len, reverse=True)
        if len(skillset) < 3:
            skillset = get_mod_skills(text)
        return skillset
    except:
        if len(skillset) < 3:
            skillset = get_mod_skills(text)
        return skillset


def get_mod_skills(text):
    exp = text.lower()
    skillset = list()
    skill_dict = {}
    nlp_text = nlp(exp)
    noun_chunks = list(nlp_text.noun_chunks)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(config.skill_csv)

    bigrams = utils.extract_ngrams(exp,2) 

    skills = list(data.columns.values)
    custom_skillset =  get_custom_skills(text)
    try:

        # check for one-grams
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)

        # check for bi-grams and tri-grams
        for token in noun_chunks:
            token = token.text.lower().strip()
            if token in skills and token not in skillset:
                skillset.append(token)
        for token in bigrams:
            if token.lower() in skills and token not in skillset:
                skillset.append(token)
        skillset = [i.lower() for i in set([i.lower() for i in skillset])]
        if len(skillset) < 5:
            for skill in custom_skillset:
                if skill not in skillset:
                    skillset.append(skill)
            try:     
                skillset = skillset[:5]
            except:
                pass       
        skillset = [i.capitalize() for i in set([i.lower() for i in skillset])]
        skillset = [i.strip() for i in skillset if not i in (' a ') ]
        skillset = sorted(skillset, key = len, reverse=True)
        return skillset
    except:
        return skillset


   
######################## GET HEAD SECTIONS #################################
def get_head_sections(data, e_val = 30, split_val = 10):
    lines = [utils.escape_ansi(line) for line in data.split('\n')]  

    
    experience_indexes, education_indexes, skills_indexes = list(), list(), list()
    PROJECT_indexes, TRAININGS_indexes, AWARDS_indexes = list(), list(), list()
    PUBLICATIONS_indexes, indexes  = list(), list()
    for index, line in enumerate(data.split('\n')):
        
        if len(line.split()) < split_val:
            ln = utils.preprocess_text(line)
            splitted = [l[:-1] for l in line.lower().split() if len(ln.lower().split())>=1]
            splitted = splitted[:3]
            check = ln.lower().split()[:3]
            if (set(check) & set(com.RESUME_SECTIONS)) or (set(splitted) & set(com.RESUME_SECTIONS)):
                words = line.split()
                indexes.append(index)


                try:
                    if ( (words[0].lower() in com.EXPERIENCE) or (words[1][:-1].lower() in com.EXPERIENCE) or (words[1].lower() in com.EXPERIENCE) or (words[2].lower() in com.EXPERIENCE) or (words[0][:-1].lower() in com.EXPERIENCE)  or (words[2][:-1].lower() in com.EXPERIENCE)):
                        experience_indexes.append(index)
                        
                except:
                    if (words[0].lower() in com.EXPERIENCE) or (words[0][:-1].lower() in com.EXPERIENCE):
                        experience_indexes.append(index)      


                try:
                    if ( (words[0].lower() in com.EDUCATION) or (words[1][:-1].lower() in com.EDUCATION) or (words[1].lower() in com.EDUCATION) or (words[2].lower() in com.EDUCATION) or (words[0][:-1].lower() in com.EDUCATION)  or (words[2][:-1].lower() in com.EDUCATION)):
                        education_indexes.append(index)
                        
                except:
                    if (words[0].lower() in com.EDUCATION) or (words[0][:-1].lower() in com.EDUCATION):
                        education_indexes.append(index)      

                try:
                    if (words[0].lower() in com.SKILLS) or (words[1].lower() in com.SKILLS) or (words[2].lower() in com.SKILLS) or (words[0][:-1].lower() in com.SKILLS) or (words[1][:-1].lower() in com.SKILLS) or (words[2][:-1].lower() in com.SKILLS):
                        
                        skills_indexes.append(index)
                except:
                    if (words[0].lower() in com.SKILLS) or (words[0][:-1].lower() in com.SKILLS):
                        skills_indexes.append(index)  

                try:
                    
                    if ((words[0].lower() in com.PROJECT) or (words[1].lower() in com.PROJECT) or (words[2].lower() in com.PROJECT) or (words[0][:-1].lower() in com.PROJECT) or (words[2][:-1].lower() in com.PROJECT) or (words[1][:-1].lower() in com.PROJECT)) and len(words) < 4:
                        PROJECT_indexes.append(index)
                except:
                    if ((words[0].lower() in com.PROJECT) or (words[0][:-1].lower() in com.PROJECT)) and len(words) < 4:
                        PROJECT_indexes.append(index) 
                        
                try:
                    
                    if ((words[0].lower() in com.AWARDS) or (words[1].lower() in com.AWARDS) or (words[0][:-1].lower() in com.AWARDS) or (words[1][:-1].lower() in com.AWARDS)) and len(words) < 4:
                        AWARDS_indexes.append(index)
                except:
                    if ((words[0].lower() in com.AWARDS) or (words[0][:-1].lower() in com.AWARDS)) and len(words) < 3:
                        AWARDS_indexes.append(index) 
                        

                try:
                    
                    if ((words[0].lower() in com.PUBLICATIONS) or (words[1].lower() in com.PUBLICATIONS)  or (words[0][:-1].lower() in com.PUBLICATIONS) or (words[1][:-1].lower() in com.PUBLICATIONS)) and len(words) < 3:
                        PUBLICATIONS_indexes.append(index)
                except:
                    if ((words[0].lower() in com.PUBLICATIONS) or (words[0][:-1].lower() in com.PUBLICATIONS)) and len(words) < 3:
                        PUBLICATIONS_indexes.append(index) 
                        
                        
                try:
                    
                    if ((words[0].lower() in com.TRAININGS) or (words[1].lower() in com.TRAININGS)   or (words[0][:-1].lower() in com.TRAININGS) or (words[1][:-1].lower() in com.TRAININGS)) and len(words) < 4:
                        TRAININGS_indexes.append(index)
                except:
                    if ((words[0].lower() in com.TRAININGS) or (words[0][:-1].lower() in com.TRAININGS)) and len(words) < 4:
                        TRAININGS_indexes.append(index)  
                        

    sections_dict = {"experience":'', "skills":'', "education":'' , 'trainings':'', 'publications':'','awards':'', 'project':''}
    
 ####################################### EXP ###############################3   
    experience_string = ''
    count = 0
    try:
        for exp in experience_indexes:
            # print(exp)
            stop = [f for f in indexes if f>exp]
            try:
                end = stop[0]
            except:
                end = len(lines)
            count = 0
            for i in range(exp,end):
                experience_string += lines[i] + '\n' 
        for e in experience_string.split('\n'):
            if len(e.split()) < 10:
                count += 1   
        flag = False
    except:
        pass
    if count < e_val:
        experience_string = ''
        _string = ''
        index_list = []
        for exp in experience_indexes:
            try:
                for i in range(200):
                    if (exp+i) not in index_list:
                        _string += lines[exp+i] + '\n'
                        index_list.append(exp+i)
            except:
                try:
                    for i in range(100):
                        if (exp+i) not in index_list:
                            _string += lines[exp+i] + '\n'
                            index_list.append(exp+i)
                except:
                    try:
                        for i in range(50):
                            if (exp+i) not in index_list:
                                _string += lines[exp+i] + '\n'
                                index_list.append(exp+i)
                    except:
                        try:
                            for i in range(20):
                                if (exp+i) not in index_list:
                                    _string += lines[exp+i] + '\n'
                                    index_list.append(exp+i)
                        except:
                            pass
            experience_string += _string
            _string = '' 
        
    sections_dict['experience'] = experience_string
    
################################### SKILLS ###########    
    
    skills_string = ''
    count = 0
    for exp in skills_indexes:
        stop = [f for f in indexes if f>exp]
        try:
            end = stop[0]
        except:
            end = len(lines)
        count = 0
        for i in range(exp,end):
            skills_string += lines[i] + '\n'
            count += 1
    if count<10:
        skills_string = ''
        for exp in skills_indexes:
            try:
                for i in range(20):
                    skills_string += lines[exp+i] + '\n'
            except:
                try:
                    for i in range(15):
                        skills_string += lines[exp+i] + '\n'
                except:
                    pass

    sections_dict['skills'] = skills_string
    
####################################### EDUCATION ###############################    
    education_string = ''
    count = 0
    for exp in education_indexes:
        stop = [f for f in indexes if f>exp]
        try:
            end = stop[0]
        except:
            end = len(lines)
        count = 0
        for i in range(exp,end):
            education_string += lines[i] + '\n'
            count += 1

    if count<5:
        education_string = ''
        _string = ''
        index_list = []
        for exp in education_indexes:
            try:
                for i in range(10):
                    if (exp+i) not in index_list:
                        _string += lines[exp+i] + '\n'
                        index_list.append(exp+i)
                        # education_string += lines[exp+i] + '\n'
            except:
                try:
                    for i in range(7):
                        if (exp+i) not in index_list:
                            _string += lines[exp+i] + '\n'
                            index_list.append(exp+i)
                except:print("Exception in education")       
            education_string += _string
            _string = ''
    sections_dict['education'] = education_string
    
############### Training ################3
    training_string = ''
    count = 0
    for exp in TRAININGS_indexes:
        stop = [f for f in indexes if f>exp]
        try:
            end = stop[0]
        except:
            end = len(lines)
        count = 0
        for i in range(exp,end):
            training_string += lines[i] + '\n'
            count += 1
    sections_dict['trainings'] = training_string

###################### Project #########################
    
    projects_string = ''
    count = 0
    for exp in PROJECT_indexes:
        stop = [f for f in indexes if f>exp]
        try:
            end = stop[0]
        except:
            end = len(lines)
        count = 0
        for i in range(exp,end):
            projects_string += lines[i] + '\n'
            count += 1
    sections_dict['project'] = projects_string

############################# Awards #######################

    awards_string = ''
    count = 0
    for exp in AWARDS_indexes:
        stop = [f for f in indexes if f>exp]
        try:
            end = stop[0]
        except:
            end = len(lines)
        count = 0
        for i in range(exp,end):
            awards_string += lines[i] + '\n'
            count += 1
    sections_dict['awards'] = awards_string
 
######################## publication ############## 
    
    publication_string = ''
    count = 0
    for exp in PUBLICATIONS_indexes:
        stop = [f for f in indexes if f>exp]
        try:
            end = stop[0]
        except:
            end = len(lines)
        count = 0
        for i in range(exp,end):
            publication_string += lines[i] + '\n'
            count += 1
    sections_dict['publications'] = publication_string
    return sections_dict


########################################## PERSONAL INFO ###################################

def get_name(entities, text):
    count = 0
    try:
        nlp = config.en_sm
        name = entities['Name']

        for n in name:
            if set(n.lower().split()) & set(comm.DESIGNATION):
                continue
            elif set(n.lower().split()) & set(comm.RESUME_SECTIONS):
                continue
            else:
                return n
        
    except:
        name = ''    
        doc = nlp(text)
        
        # Extract entities
        doc_entities = doc.ents

        doc_persons = filter(lambda x: x.label_ == 'PERSON', doc_entities)
        doc_persons = filter(lambda x: len(x.text.strip().split()) >= 2, doc_persons)
        doc_persons = list(doc_persons)
        if len(doc_persons) > 0: 
            name = str(doc_persons[0])
            return name
            
        
        else:
            lines = utils.tokenize_text(text)
            
            for sentence in lines:
                entities = nltk.chunk.ne_chunk(sentence)
                for subtree in entities.subtrees():
                    if subtree.label() == 'PERSON':
                        for leaf in subtree.leaves():
                            name = leaf[0]
                            name = str(name)
                            return name
            return "No Name Found"



## Function for emailid
def get_email(text):
    pattern = re.compile(r'\S*@\S*[.]\w*')
    match = pattern.findall(text)
    req_match = []
    symbols = [':', '(', ')', ',', '=','#']

    for each in match:
        flag = False
        index = []

        for e in symbols:
            if each.find(e) != -1:
                flag = True
                index.append(each.find(e))
        if flag == True:
            req = max(index)
            req_match.append(each[req+1:])
            match = req_match
    try:
        match =match[0]
    except:pass

    return((match))

def get_gender(text):
    text = nlp(text)
    tokens = [token.text.lower().strip() for token in text]   

    if 'female' in tokens:
        gender = 'Female'
    elif 'male' in tokens:
        gender = 'Male'
    else:
        gender = 'not mentioned'
    return gender


def get_personal(custom_entities, data):
    
    name = ""
    emailid = get_email(data)
    name = get_name(custom_entities, data)
    if (name==None or name=='None'):
        name = ner(data)
    phoneno = get_phonenumber(data)
    gender = get_gender(data)
    try:
        location = str(get_location(data, custom_entities))
    except:
        location = 'None'

    
    pincode  = get_pincode(data)
    dob = get_dob(data, custom_entities)
    
    personal = {
            "Name" : name,
            "Phone Number": phoneno,
            "Email Id" : emailid,
            "Gender"   : gender,
            "Date of birth" : dob,
            "Location" : location,
            "Pincode"  : pincode
        }   

    return personal


def get_pincode(text):
    pincode =  r"[^\d][^a-zA-Z\d](\d{6})[^a-zA-Z\d]"
    pattern = re.compile(pincode)
    result = pattern.findall(text)
    if len(result)==0:
        return ' '
    return result[0]

                            
def get_dob(text, ents):
    

        dob = 'Not found'
        lines = [line.strip() for line in text.split('\n')]
        dob_pattern = r'((\d)?(\d)(th)?.((jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)|(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)|(\d{2})).(\d{4}))'
        required = ''
        matches = ['dob', 'date of birth', 'birth date']
        flag = 0
        count = 0
        for lin in lines:
            
            if any(x in lin.lower().strip() for x in matches):
                required = lin.lower() +'\n'
                flag = 1
            if flag == 1:
                if len(lin.split()) < 1:continue
                required += lin.lower() + '\n'
                count +=1
            if count > 4:
                break        
        required = ' '.join(req for req in required.split())

        match = re.findall(dob_pattern, required)
        try:
            return match[0][0]
        except:
            return ''


## Function for location:
def get_location(text, ents):
    nations = pd.read_csv(config.nations)
    country = pd.read_csv(config.country)
    state = pd.read_csv(config.state)


    nations = list(nations.columns.values)
    state = list(state.columns.values)
    country = list(country.columns.values)
    nationality = 'Not found'
    loc_extended = []
    with open(config.city, 'r') as f:
        for line in f:
            cities =  line.split(',')   
    lines = [line for line in text.split('\n')]


    for line in lines:
        if len(line) == 0:continue
        for word in line.split():
            word =  re.sub(r'[^\w\s]',' ',word)
            if word.lower().strip() in comm.LOCATION:
                
                words = [w for w in line.split() if w in nations]
                if len(words) != 0:
                    for nat in nations:
                        if nat.lower().strip() in line.lower().strip():

                            return nat
                
                words = [w for w in line.split() if w in country]
                if len(words) != 0:
                    for loc in country:
                        if loc.lower().strip() in line.lower().strip() :
                            return loc
                
                for each in cities:
                    if each in line.lower().strip().split():
                        return each.capitalize()
                
    
    text = nlp(text)
    tokens = [token for token in text]
    locations_captured = list(set([(entity) for sent in text.sents for entity in sent.ents if entity.label_=='GPE']))
 
    state = [n.lower() for n in state]
    country = [n.lower() for n in country]
     
    _nationality = list()
    locations_captured = sorted(locations_captured, key=lambda x:x[1])
    
    for each in locations_captured:
            if str(each).lower() in cities:
                return each

    for each in locations_captured:
        if each.text.lower().strip() in state  or each.text.lower().strip() in country or str(each).lower() in cities:
            try:
                return each.text 
            except:
                return each


   
    return ''

## Function for phonenumber
def get_phonenumber(text):
    number = []
    try:
        pattern = re.compile(r'([+(]?\d+[).\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        match = pattern.findall(text)
        match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
        match = [re.sub(r'\D$', '', el).strip() for el in match]
        match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
        try:
            for el in list(match):
                if len(el.split('-')) > 3: continue 
                for x in el.split("-"):
                    try:
                        if x.strip()[-4:].isdigit():
                            if int(x.strip()[-4:]) in range(1900, 2100):
                                match.remove(el)
                    except:
                        pass
        except:
            pass
        number = match
    except:
        pass
    
    new_number = []
    
    for num in number:
        out = re.sub(r'[^0-9]+', '', num)
        if len(out)>9:
            new_number.append(num)
            continue
    number = new_number
    
    validated_number = []
    data = pd.read_csv('models/phoneno.csv')
    for num in number:
        for ind in data.index:
            try:
                z = phonenumbers.parse(num, data['Code'][ind])
                result = phonenumbers.is_valid_number(z)
            except:
                result = False
            
            if result == True and num not in validated_number:
                validated_number.append(num)
    number = validated_number

    
    try:
        number = [number[0]]#, number[1]]
    except:
        try:
            number = [new_number[0]]
        except:
            pass
################## FROM ENTITIES ######################

    # custom_ents = get_custom_entities(text)
    # count = 0
    # try:
    #     no = custom_ents['Phone Number']
    #     print(no)
    #     number = []
    #     for num in no:
    #         out = re.sub(r'[^0-9]+', ' ', num)
    #         # print(num, out)
    #         if len(out)>9:
    #             number.append(out)
    #             count += 1
    #             if count > 1:break
    #     return number
    # except:
    #     pass

    
    return number

#################### Reference ###################
def get_reference(text):
    flag = False
    new_data = ''
    count = 0
    req = [lines for  lines in text.split('\n')]
    for r in req:
        if ('reference' in r.lower() or 'references' in r.lower()) and len(r.split())<=2:
            flag = True
        if flag == True and count<50:
            new_data += r + '\n'
            count += 1
    # print(new_data)
    ref_names = list()
    doc = nlp(new_data)
    for d in doc.ents:
        if d.label_ == 'PERSON':
            ref_names.append(d.text)
    designation = []
    lines =  [e for e in new_data.split('\n')]
    
    pattern = 'CHUNK: {<NNS>?<NNS>?<NN>?<NN>?<JJ>?<CC>?<DT>?<NN|NNP.*><IN>?<NNP>*<NNS>?<CC>?<NN>*<NNP.*>*}'
    cp =   nltk.RegexpParser(pattern)
    exp = []
    prob_exp=[]
    for line in lines:
        line = utils.preprocess(line)
        if len(line) == 0:continue
        cs = cp.parse(line)
        for n in cs:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'CHUNK':
                    if len(n.leaves()) > 1:
                        req = ''
                        for leaf in n.leaves():
                            req += leaf[0]+' '
                        req = req[:-1]
                        exp.append(req)
                    elif len(n.leaves()) ==1:
                        req = ''
                        for leaf in n.leaves():
                            req += leaf[0]+' '
                        req = req[:-1]
                        prob_exp.append(req)

    designation = []
    for each in exp:
        each1 =  re.sub(r'[^\w\s]',' ',each)
        if set(each1.lower().split()) & set(com.DESIGNATION):
            designation.append(each)
    for each in prob_exp:
        if set(each.lower().split()) & set(com.DESIGNATION_ONE):
            designation.append(each)   
    
    
    new_designation, ll = [], []
    for ind, line in enumerate(new_data.split('\n')):
        for des in designation:
            if des.strip() in line:
                
                if ind not in ll:
                    new_designation.append(des)   
                    ll.append(ind)
                    
    # designation = new_designation
    emailids = get_email(new_data)
    phn = get_phonenumber(new_data)

    reference = []    
    for name in ref_names:
        try:
            des = designation[0]
            designation.remove(designation[0])
        except:
            des = ''
        try:
            em = emailids[0]
            emailids.remove(emailids[0])
        except:
            em = ''
        try:
            ph = phn[0]
            phn.remove(phn[0])
        except:
            ph = ''
        
        reference.append({"Name": name, "Desingation":des, "Emailid":emailids, "Phone Number":ph}) 
    return  reference

