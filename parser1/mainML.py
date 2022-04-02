import os
import textract
from parser1 import MLresume_extraction
from parser1.commons import constants as comm
import json
import shutil
from parser1 import model_extraction
from parser1 import config_p
import utils
from tika import parser
from parser1.fileconversion1 import fileconversion11


class Extract:
    def __init__(self, _file):
        # try:
        # text,text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = fileconversion11(_file,y=0)
        # text=fileconversion11(_file, y=0)
        # self.data = str(text)
        raw = parser.from_file(_file)
        self.data =  raw['content']
        self.new_data = utils.get_new_data(self.data)
        self.filename = _file.split('/')[-1]

        print("----------------------")
        print(self.filename)

        self.custom_entities = utils.get_custom_entities(self.data)

        self.lang = MLresume_extraction.get_lang(self.data)
        self.personal_info = MLresume_extraction.get_personal(
            self.custom_entities, self.data)

        self.toe = MLresume_extraction.get_total_years(self.data)

        self.experience, self.cjp = model_extraction.get_experience(
            self.new_data)

        self.education = model_extraction.get_education(self.new_data)
        self.awards = MLresume_extraction.get_extra(self.data, 'awards')
        self.skills = MLresume_extraction.get_skills(
            self.custom_entities, self.data)

        self.reference = MLresume_extraction.get_reference(self.data)

        self.details = {"FileName": self.filename,
                        "File Language": self.lang,
                        "Personal Details": self.personal_info,
                        "Current Job": self.cjp,
                        "Total Experience(years)": self.toe,
                        "Experience": self.experience,
                        "Education": self.education,
                        "Skills": self.skills,
                        "Reference": self.reference,
                        "Awards": self.awards
                        # "Other Information extracted:":self.others
                        }
        # print(self.details)
        print(json.dumps(self.details))
        # except:

        #     self.details = {"Message":"Some error occured"}

    def get_details(self):
        return (self.details)


def get_extracted(_file):
    parser = Extract(_file)
    return parser.get_details()


def get_parsed(file_name):
    dir_path = config_p.basepath
    file_path = os.path.join(dir_path, config_p.filedir, file_name)
    results = get_extracted(file_path)
    return results


def delete():
    dirpath = os.path.join(config_p.basepath, config_p.filedir)
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
    try:
        shutil.rmtree(filepath)
    except OSError:
        os.remove(filepath)


if __name__ == '__main__':

    file_path = os.path.join(config_p.basepath, config_p.filedir)
    results = [get_extracted(os.path.join(file_path, _file))
               for _file in os.listdir(file_path)]
