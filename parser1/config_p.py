import os
import spacy


basepath = os.path.dirname(os.path.realpath(__file__))
filedir = "/Users/cosmos/Desktop/DP/backend/resume_parser_nlp 2.2.4/samples"
skill_csv  = 'parser1/commons/skills.csv'
nations = 'parser1/commons/nationality.csv'
state = 'parser1/commons/state.csv'
country ='parser1/commons/country.csv'
city = "parser1/commons/cities_samples.txt"

skills_rb = 'parser1/commons/skills'
skill_model_dir = os.getcwd() + '/parser1/commons/Models/SKILLS_MODEL'
resume_model = os.getcwd() + '/parser1/commons/Models/RESUME-REAL_MODEL'
education_model = 'parser1/commons/Models/NEW_EDUCATION'
experience_model = 'parser1/commons/Models/NEW_EXPERIENCE'


en_sm = spacy.load('en_core_web_sm')
