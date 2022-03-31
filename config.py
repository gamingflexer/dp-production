import torch
import os
import spacy
basepath = os.path.dirname(os.path.realpath(__file__))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#change accordinly
summary_model = '/Users/cosmos/Documents/DP-ref/Summary-100'
bert_dict_path = "/home/aiworkstation2/Music/ser/DeepBlue/flask/models/model_e10.tar"
index = "/"
driver_path = "/Users/cosmos/chromedriver"

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#not to change
spacy_700_path = os.path.join(basepath,"models/DP/new")
f2 = os.path.join(basepath,"static","zip","files/")
e2 = os.path.join(basepath,"static","zip","extracted/")
z2 = os.path.join(basepath,"static","zip/")

ZIPPED = os.path.join(basepath,"static","zip")
EXTRACTED = os.path.join(basepath,"static","zip","extracted")
UPLOAD_FOLDER =  os.path.join(basepath,"static","zip","files")

filedir = "/Users/cosmos/Desktop/DP/backend/resume_parser_nlp 2.2.4/samples"
skill_csv  = 'models/skills.csv'
nations = 'models/nationality.csv'
state = 'models/state.csv'
country ='models/country.csv'
city = "models/cities_samples.txt"

skills_rb = 'models/skills'
skill_model_dir = os.getcwd() + '/models/SKILLS_MODEL'
resume_model = os.getcwd() + '/models/RESUME-REAL_MODEL'
education_model = 'models/NEW_EDUCATION'
experience_model = 'models/NEW_EXPERIENCE'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# spacy
# spacy_700_path = 'C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\models\\new'
# spacy_skills_path = 'models\\Models-Seprate-700\\SKILL'
# spacy_edu_path = 'models\\Models-Seprate-700\\EDU'
# spacy_exp_path = 'models\\Models-Seprate-700\\EXP'

# spacy_m2 = ""
# summary_model = ""


# # BERT
# # BERT
# MAX_LEN = 500 #512
# DEVICE = torch.device("cpu")
# MODEL_PATH = 'bert-base-uncased'
# bert_dict_path = "/home/aiworkstation2/Music/ser/DeepBlue/flask/models/model_e10.tar"


# #flask
# ZIPPED = "C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\static\\zip"
# EXTRACTED = "C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\static\\extracted"
# UPLOAD_FOLDER = "C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\static\\files"

# f2 = "C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\static\\files\\"
# e2 = "C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\static\\extracted\\"
# z2 = "C:\\Users\\Yash\\OneDrive\\Desktop\\DeepBlue\\flask\\static\\files\\zip\\"
# index = "\\"

driver_path = ""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

#Om

#BERT
# MAX_LEN = 500 #512
# DEVICE = torch.device("cpu")
# MODEL_PATH = 'bert-base-uncased'

# spacy_skills_path = '/Users/cosmos/Desktop/DeepBlue/flask/models/Models-Seprate-700/SKILL'
# spacy_edu_path = '/Users/cosmos/Desktop/DeepBlue/flask/models/Models-Seprate-700/EDU'
# spacy_exp_path = '/Users/cosmos/Desktop/DeepBlue/flask/models/Models-Seprate-700/EXP'

# if docker == 0:
#     os.system("docker run -d -p 9998:9998 logicalspark/docker-tikaserver")
#     docker = docker + 1
# else:
#     print("Docker already running")




