import spacy
import re
import json
from parser1.mainML import MLresume_extraction as RE
import string
from parser1 import config_p
from parser1 import utils


def get_custom_entities_eduexp(text, type):
    if type == "education":
        model_dir =  config_p.education_model
    else:
        model_dir =  config_p.experience_model
    nlp2 = spacy.load(model_dir)
    doc2 = nlp2(text)
    entities = utils.extract_entities(doc2)
    for key, val in entities.items():
        entities[key] = utils.clean_text(val)            
    return entities



def get_education(text):
    try:

        degree, college, during = [],[], []
        education = {}
        new_text = RE.get_head_sections(text)['education']
        education = get_custom_entities_eduexp(new_text, "education")
        
        
        if 'Degree' not in education:
            education_whole = get_custom_entities_eduexp(new_text, "education")
            education = education_whole
            new_text = text        
        
        
            
        try:
            degree  = [edu for edu in education['Degree'] if len(edu.split())<10]
            for edu in education['Degree']:
                if len(edu.split())>=10:
                    ll = edu.split()
                    add = ' '.join(l for ind, l in enumerate(ll) if ind<=10)
                    degree.append(add)
        except:print("Exception-Degree")
        try:
            college = [col for col in education['College Name'] if len(col.split())<10]
            for edu in education['College Name']:
                if len(edu.split())>=10:
                    ll = edu.split()
                    add = ' '.join(l for ind, l in enumerate(ll) if ind<8)
                    college.append(add)
            
        except:print("Exception-College")
        try:
            during = [col for col in education['Graduation Year'] if len(col.split())<10]
            for dur in education['Graduation Year']:
                if len(dur.split())>=10:
                    ll = dur.split()
                    add = ' '.join(l for ind, l in enumerate(ll) if ind<8)
                    during.append(add)
        except:print("Exception-Graduation Year")

        college_index, degree_index, during_index = [], [], []
        extra_degree, extra_college, extra_during  = [], [], []
        durings, colleges, degrees = [], [], []
        deg_indexes = []
        add = []

        for deg in degree:  
            for ind, line in enumerate(new_text.split('\n')):  
                if ind in add:
                    continue
                flag = check_match(deg, line)

                if flag == True:
                    degree_index.append((deg, ind))
                    flag = False
                    degrees.append(deg)
                    deg_indexes.append(ind)
                    add.append(ind)
                    break
        try:
            low = min(deg_indexes) - 5
            high = max(deg_indexes) + 5
        except:
            low = 0
            high = len(new_text.split('\n'))

        add = []
        for col in college:
            for ind, line in enumerate(new_text.split('\n')):
                if ind in add:
                    continue
                if ind > low and ind <high: 
                    flag = check_match(col, line)
                    if flag == True:
                        college_index.append((col, ind))
                        flag = False
                        colleges.append(col)
                        add.append(ind)
                        break
        add = []
        for dur in during: 
            for ind, line in enumerate(new_text.split('\n')):
                if ind in add:
                    continue
                if ind > low and ind <high:
                    flag = check_match(dur, line)
                    if flag == True:
                        during_index.append((dur, ind)) 
                        flag = False
                        durings.append(dur)
                        add.append(ind)
                        break
                    
        degree_index = sorted(degree_index, key = lambda x: x[1])
        college_index = sorted(college_index, key = lambda x: x[1])
        during_index = sorted(during_index, key = lambda x: x[1])
        
        for each in degree:
            if each not in degrees:
                extra_degree.append(each)
        for each in college:
            if each not in colleges:
                extra_college.append(each)
        for each in during:
            if each not in durings:
                extra_during.append(each)        
                
        extra_degree = list(set(extra_degree))
        extra_college = list(set(extra_college))
        extra_during = list(set(extra_during))
        
        degree = [each[0] for each in degree_index]
        college = [each[0] for each in college_index]
        during = [each[0] for each in during_index]
        
        
        for each in extra_degree:
            degree.append(each)
        for each in extra_college:
            college.append(each)
        for each in extra_during:
            during.append(each)
            
        new_education = { "Degree" : degree,
                            "College" : college,
                            "Graduation Year": during
        }
        
        new_education['Trainings/Courses'] = RE.get_extra(text, 'trainings')
        new_education['Publications'] = RE.get_extra(text, 'publications')
        

        return new_education
    except:
        print("Exception..")
        return ''


def get_experience(text):
    try:
        new_experience = {}
        new =''
        experience = ''
        new_text = RE.get_head_sections(text)['experience']
        designation,company, during = [],[], []
        experience = get_custom_entities_eduexp(new_text, "experience")
       
        if 'Designation' not in experience:
            
            new_text = RE.get_head_sections(text,30, 20)['experience']
            experience = get_custom_entities_eduexp(new_text, "experience")

            
        experience_whole = get_custom_entities_eduexp(new_text, "experience")
        try:
            for exp in experience_whole['Designation']:
                if exp not in experience['Designation']:
                    experience['Designation'].append(exp)
        except:print("exception in full text experience")
        
        if 'Designation' not in experience:
            experience = experience_whole
            new_text = text
            
        try:
            designation  = [ exp for exp in experience['Designation'] if len(exp.split())<10]
            
            for edu in experience['Designation']:
                if len(edu.split())>=10:
                    ll = edu.split()
                    add = ' '.join(l for ind, l in enumerate(ll) if ind<=10)
                    designation.append(add)
        except:print("Exception-Desingation")
        try:
            company = [comp for comp in experience['Companies worked at'] if len(comp.split())<10]
            for edu in experience['Companies worked at']:
                if len(edu.split())>=10:
                    ll = edu.split()
                    add = ' '.join(l for ind, l in enumerate(ll) if ind<=10)
                    company.append(add)
        except:print("Exception-Companies Worked at")
        try:
            during = [dur for dur in experience['Years of Experience'] if len(dur.split())<10]
            for dur in experience['Years of Experience']:
                if len(dur.split())>=10:
                    ll = dur.split()
                    add = ' '.join(l for ind, l in enumerate(ll) if ind<=10)
                    during.append(add)
        except:print("Exception-Years Of experience")

        
        company_index, designation_index,during_index  = [], [], []
        extra_designation, extra_company, extra_during  = [], [], []
        designations, companies, durings = [], [], []
        des_indexes = []
        
        add = []
        for des in designation:
            for ind, line in enumerate(new_text.split('\n')):
                if ind in add:
                    continue
                flag = check_match(des, line)
                if flag == True:
                    designation_index.append((des, ind))
                    flag = False
                    designations.append(des)
                    des_indexes.append(ind)
                    add.append(ind)
                    break
                
        try:
            low = min(des_indexes) - 8
            high = max(des_indexes) + 15 
        except:
            low = 0
            high = len(new_text.split('\n'))

        add = []
        for com in company:
            for ind, line in enumerate(new_text.split('\n')):
                if ind in add:
                    continue
                if ind>low and ind<high: 
                    flag = check_match(com, line)

                    if flag == True:
                        company_index.append((com, ind))
                        flag = False
                        companies.append(com)
                        add.append(ind)
                        break
        add = []
        for dur in during:
            for ind, line in enumerate(new_text.split('\n')):
                if ind in add:
                    continue
                if ind>low and ind<high: 
                    flag = check_match(dur, line)
                    if flag == True:
                        during_index.append((dur, ind))
                        flag = False
                        durings.append(dur) 
                        add.append(ind)
                        break
        designation_index = sorted(designation_index, key = lambda x: x[1])
        company_index = sorted(company_index, key = lambda x: x[1])
        during_index = sorted(during_index, key = lambda x: x[1])


        for each in designation:
            if each not in designations:
                extra_designation.append(each)
        for each in company:
            if each not in companies:
                extra_company.append(each)
        for each in during:
            if each not in durings:
                extra_during.append(each)
        
        extra_designation = list(set(extra_designation))
        extra_company = list(set(extra_company))
        extra_during = list(set(extra_during))       
       
       
        designation = [each[0] for each in designation_index]
        company = [each[0] for each in company_index]
        during = [each[0] for each in during_index]
       
       
        for each in extra_designation:
            designation.append(each)
        for each in extra_company:
            company.append(each)
        for each in extra_during:
            during.append(each)
            
        new_experience = { "Designation" : designation,
                           "Company" : company,
                           "Experience Year": during
        }       
       
        
        new_experience['Projects'] = RE.get_extra(text, 'project')
        try:
            CJP = designation_index[0][0]
            if len(CJP) == 0:
                CJP = RE.get_custom_entities(text)['Current Job Position'][0]    
        except:
            CJP = ''
            print("no current job")
        return new_experience, CJP

    except:
        print("Exception")
        return '', ''
    
    
def check_match(req, line):
    
     
    line = re.sub(r'[^0-9a-zA-Z]+', ' ', line).lower().strip()
    req = re.sub(r'[^0-9a-zA-Z]+', ' ',req).lower().strip()
    # print(line, "...", req)
    count = 0
    sub_req =''
    flag = False

    if req in line:
        # print(req)
        return True 

    if len(req.split()) > 6:
        for r in req.split():
            if count >= 5:
                break
            sub_req += r
            count += 1
        flag = True
        if sub_req in line:
            
            return True        
     
    req_list = req.split()
    count = 0
    if len(req.split()) > 4:

        for each in req_list:
            if each in line:
                count += 1
        if count/len(req_list) > 0.9:
            # print(count/len(req_list), req, line)
            return True
    count = 0
    if len(req.split()) > 8:
        
        f_req = req.split()[:5]
        l_req = req.split()[5:]
        for each in f_req:
            if each in line:
                count += 1
        if count+1 >= len(f_req):
            return True
        count = 0
        for each in l_req:
            if each in line:
                count += 1
        if count+1 >= len(l_req):
            return True
                
    return False
    