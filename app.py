from flask_ngrok import run_with_ngrok
from constants import *
from ast import Return
from flask import Flask, render_template, request, flash, redirect
from flask import *
import os
import shutil
import ast
import pymysql
import requests as rq
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import mysql
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
import pyperclip
import subprocess
import urllib.request
import zipfile
import MySQLdb.cursors
import sys
from flask_mysqldb import MySQL
import mysql.connector
from werkzeug.utils import secure_filename
import pyunpack
import urllib.request
from keras.preprocessing.sequence import pad_sequences
from simplet5 import SimpleT5
from modeldb import*
from fileconversion import fileconversion0000
from preprocessing import*
from preprocessing import dict_clean
from linkedIn import linked_in_scrap
from githubs import github_scrape
from model import*
from db import *
from config import *
from flask_fun import * 
from constants import *
from ranking import cosine_sim,ranking
from linkedlndict import *
from model import parser



# BERT

print('\nModel Loaded!\n')

model_summary = SimpleT5()
model_summary.from_pretrained(model_type="t5", model_name="t5-large")
model_summary.load_model(summary_model, use_gpu=False)

# Summary_run()
# learn.load(summary_extractive)

# tokenizer_bert_ner = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model_bert_ner = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
print('\n NER Model & Summary Loaded!\n')

# flask
app = Flask(__name__)
#run_with_ngrok(app)
# app.config['ENV'] = 'development'
# app.config['DEBUG'] = True
# app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['MYSQL_HOST'] = 'dpomserver.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'dpomserver@dpomserver'
# app.config['MYSQL_HOST'] = 'Localhost'
# app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Yashw@123'
app.config['MYSQL_DB'] = 'deepbluecomp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['ZIPPED'] = ZIPPED
app.config['EXTRACTED'] = EXTRACTED
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print('\nFlask Started!\n')

@app.route('/', methods=["POST", "GET"])
def login():

    return render_template('loginpage.html', passconditions='False', conditions='False')


@app.route('/signup', methods=["POST", "GET"])
def signup():
    return render_template('signup.html')

@app.route('/verify', methods=["POST", "GET"])
def verify():
    table_pass = []
    print("under verify")
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        email = request.form.get("emailid")
        # print(email)
        password = request.form.get("pass")
        # print(password)
        verify = cur.execute(
            "Select password from login WHERE emailid= %s ", (email,))
        print('database')
        if verify > 0:
            row = cur.fetchall()
            for dict in row:
                table_pass.append(list(dict.values()))
            print(table_pass)
            print(str(table_pass[0][0]))
            print(password)

            if (str(password) == str(table_pass[0][0])):
                print("in if")
                return render_template('Homepage.html')
            else:
                return render_template('loginpage.html', passconditions='True')

        else:
            return render_template('loginpage.html', conditions='True')
    mysql.connection.commit()
    cur.close()


@app.route('/user', methods=["POST", "GET"])
def candiate():

    cur = mysql.connection.cursor()
    if request.method == 'POST':
        email = request.form.get("emailid")
        passw = request.form.get("pass")
        repassw = request.form.get("repass")
        print(email, passw, repassw)
        if(passw == repassw):
            print("underif")
            cur.execute(
                "INSERT INTO login(emailid,password) VALUES (%s, %s)", (email, passw,))
            mysql.connection.commit()
            cur.close()
            return redirect('/')
        else:
            return render_template('signup.html', repassconditions='True')


@app.route('/home', methods=["POST", "GET"])
def hello():
    return render_template('Homepage.html')


@app.route('/upload2', methods=["POST", "GET"])
def upload2():
    return render_template('upload2.html')


@app.route("/upload", methods=['POST', 'GET'])
def upload():


    dirzip_list = os.listdir(app.config['ZIPPED'])

    for zipfileli in dirzip_list:
        os.remove(z2 + zipfileli)

    dirrar_list = os.listdir(app.config['EXTRACTED'])

    for rarfileli in dirrar_list:
        os.remove(e2 + rarfileli)

    folder = f2
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print('\n upload running \n')


    cur = mysql.connection.cursor()
    #cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
       # name = request.form.get('first name')
        #last = request.form.get('Last name')
        #mail = request.form.get('email')
        #addno = request.form.get('Admissionno')
        if 'files[]' not in request.files:
            flash("No file part")
            return redirect(request.url)
        files = request.files.getlist('files[]')
        print(files)
        val = 1

       # enumerate(list)

        for file in files:

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                print(file.filename)
                name = ((file.filename).rsplit('.'))[1]
                if (name == 'zip'):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['ZIPPED'], filename))
                    zip_ref = zipfile.ZipFile(os.path.join(
                        app.config['ZIPPED'], filename), 'r')
                    zip_ref.extractall(app.config['EXTRACTED'])
                    dir_list = os.listdir(app.config['EXTRACTED'])
                    print(dir_list)
                    for i in dir_list:
                        original = e2 + str(i)
                        x = original.rindex(index)
                        y = original.rindex(".")
                        num = str(val)
                        val = val + 1
                        path = original[:x + 1] + "resume" + num + original[y:]
                        filerename = "resume" + num + original[y:]
                        os.rename(original, path)
                        binartfile = convertToBinary(path)
                        # moving on to final folder
                        cur.execute("INSERT INTO deepbluecomp_table(files_path,binaryfiles_path) VALUES (%s, %s)",
                                    (filerename, binartfile))
                        print("------zip")
                        text1, link, mailid, ftext = fileconversion0000(
                                path, num)
                        linkdedln, github, others = get_links(link)
    
                        cur.execute(
                                "INSERT INTO parse( extracted_text, cleaned_text,emails, linkedin_link, github_link,extra_link) VALUES (%s, %s, %s, %s, %s, %s )",
                                (text1, ftext, mailid, linkdedln, github, others,))
    
                        mysql.connection.commit()
                        print("\n------MODELS--------\n")
                        outparsed = parser(path)
                        print("out:",outparsed)
                        cur.execute(
                                "INSERT INTO modelfinal( Name, Phone_Number,Email_id,Gender, DOB,Location,Pincode,Current_Job,TExperience,Designation,Company,Experience_Year,Projects,Degrees,College,YearOfPassout,Courses,Publication,Skills,Referr,Awards,University,Degree,CompaniesWorkedat) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,%s,%s, %s, %s,%s)",
                                ((personal1(outparsed.get('Personal Details')),) ,(personal2(outparsed.get('Personal Details')),) ,(personal3(outparsed.get('Personal Details')),), (personal4(outparsed.get('Personal Details')),), (personal5(outparsed.get('Personal Details')),) ,(personal6(outparsed.get('Personal Details')),),(personal7(outparsed.get('Personal Details'))) ,(cjob(outparsed),),(totalexp(outparsed),) ,(experdetails1(outparsed.get('Experience')),),(experdetails2(outparsed.get('Experience')),) ,(experdetails3(outparsed.get('Experience')),) ,(experdetails4(outparsed.get('Experience')),),(edudetails1(outparsed.get('Education')),) ,(edudetails2(outparsed.get('Education')),),(edudetails3(outparsed.get('Education')),),(edudetails4(outparsed.get('Education')),) ,(edudetails5(outparsed.get('Education')),) ,(skilldetails(outparsed.get('Skills')),),(refdetails(outparsed.get('Reference')),),(award(outparsed.get('Awards')),),(university(outparsed.get('university')),),(degrees(outparsed.get('degree')),),(cwat(outparsed.get('Companies worked at')),)   ,))
                        mysql.connection.commit()
                    #     text, link, mailid, ftext = fileconversion0000(
                    #         path, num)
                    #     linkdedln, github, others = get_links(link)

                    #     cur.execute(
                    #         "INSERT INTO parse( extracted_text, cleaned_text,emails, linkedin_link, github_link,extra_link) VALUES (%s, %s, %s, %s, %s, %s )",
                    #         (text1, ftext, mailid, linkdedln, github, others,))

                    dir_list = os.listdir(app.config['EXTRACTED'])
                    for file_name in dir_list:
                         source = e2 + file_name
                         destination = f2 + file_name
                         shutil.move(source, destination)


                    # for entity in entities:
                    #     if entity in oo2.keys():
                    #         values = oo2.get(entity)
                    #         if (entity.replace(" ", "_").lower() in databaseattribute.keys()):
                    #             databaseattribute.update(
                    #                 {entity.replace(" ", "_").lower(): values})

                    # # print(databaseattribute)
                    # for key, values in databaseattribute.items():
                    #     if (databaseattribute[key] == None):
                    #         databaseattribute[key] = 'Null'

                    # cur.execute("INSERT INTO model(unknown,name,degree,skills,college_name,university,graduation_year,companies_worked_at,designation,years_of_experience,location,address,rewards_achievements,projects) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    #             (databasevalue(databaseattribute.get('unknown')), databasevalue(databaseattribute.get('name')), databasevalue(databaseattribute.get('degree')), databasevalue(databaseattribute.get('skills')), databasevalue(databaseattribute.get('college_name')), databasevalue(databaseattribute.get('university')), databasevalue(databaseattribute.get('graduation_year')), databasevalue(databaseattribute.get('companies_worked_at')), databasevalue(databaseattribute.get('designation')), databasevalue(databaseattribute.get('years_of_experience')), databasevalue(databaseattribute.get('location')), databasevalue(databaseattribute.get('address')), databasevalue(databaseattribute.get('rewards_achievements')), databasevalue(databaseattribute.get('projects')),))

                    # cur.execute(
                    #     "INSERT INTO list(email) VALUES (%s)", (mailid,))

                    # for key, values in databaseattribute.items():
                    #     databaseattribute[key] = 'Null'

                elif(name == 'rar'):
                    filename = secure_filename(file.filename)
                    print(type(filename))
                    file.save(os.path.join(app.config['ZIPPED'], filename))

                    #zip_ref = zipfile.ZipFile(os.path.join(app.config['ZIPPED'], filename), 'r')
                    rarpath = pyunpack.Archive(
                        os.path.join(app.config['ZIPPED'], filename))
                    rarpath.extractall(app.config['EXTRACTED'])

                    dir_list = os.listdir(app.config['EXTRACTED'])
                    for i in dir_list:
                        original = e2 +  str(i)
                        x = original.rindex(index)
                        y = original.rindex(".")
                        num = str(val)
                        val = val + 1
                        path = original[:x + 1] + "resume" + num + original[y:]
                        filerename = "resume" + num + original[y:]
                        os.rename(original, path)

                        binartfile = convertToBinary(path)

                        cur.execute("INSERT INTO deepbluecomp_table(files_path,binaryfiles_path) VALUES (%s, %s)",
                                    (filerename, binartfile))
                        print("------")
                        text1, link, mailid, ftext = fileconversion0000(
                                path, num)
                        linkdedln, github, others = get_links(link)
    
                        cur.execute(
                                "INSERT INTO parse( extracted_text, cleaned_text,emails, linkedin_link, github_link,extra_link) VALUES (%s, %s, %s, %s, %s, %s )",
                                (text1, ftext, mailid, linkdedln, github, others,))
    
                        mysql.connection.commit()
                        print("\n------MODELS--------\n")
                        outparsed = parser(path)
                        print("out:",outparsed)
                        cur.execute(
                                "INSERT INTO modelfinal( Name, Phone_Number,Email_id,Gender, DOB,Location,Pincode,Current_Job,TExperience,Designation,Company,Experience_Year,Projects,Degrees,College,YearOfPassout,Courses,Publication,Skills,Referr,Awards,University,Degree,CompaniesWorkedat) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,%s,%s, %s, %s,%s)",
                                ((personal1(outparsed.get('Personal Details')),) ,(personal2(outparsed.get('Personal Details')),) ,(personal3(outparsed.get('Personal Details')),), (personal4(outparsed.get('Personal Details')),), (personal5(outparsed.get('Personal Details')),) ,(personal6(outparsed.get('Personal Details')),),(personal7(outparsed.get('Personal Details'))) ,(cjob(outparsed),),(totalexp(outparsed),) ,(experdetails1(outparsed.get('Experience')),),(experdetails2(outparsed.get('Experience')),) ,(experdetails3(outparsed.get('Experience')),) ,(experdetails4(outparsed.get('Experience')),),(edudetails1(outparsed.get('Education')),) ,(edudetails2(outparsed.get('Education')),),(edudetails3(outparsed.get('Education')),),(edudetails4(outparsed.get('Education')),) ,(edudetails5(outparsed.get('Education')),) ,(skilldetails(outparsed.get('Skills')),),(refdetails(outparsed.get('Reference')),),(award(outparsed.get('Awards')),),(university(outparsed.get('university')),),(degrees(outparsed.get('degree')),),(cwat(outparsed.get('Companies worked at')),)   ,))
                        mysql.connection.commit()
                    #     text,scraplink, eid, ftext= fileconversion0000(path, num)
                    #     text, link, mailid, ftext = fileconversion0000(
                    #         path, num)
                    #     linkdedln, github, others = get_links(link)

                    #     cur.execute(
                    #         "INSERT INTO parse( extracted_text, cleaned_text,emails, linkedin_link, github_link,extra_link) VALUES (%s, %s, %s, %s, %s, %s )",
                    #         (text1, ftext, mailid, linkdedln, github, others,))

                    #     # moving on to final folder
                    dir_list = os.listdir(app.config['EXTRACTED'])
                    for file_name in dir_list:
                        source = e2 + file_name
                        destination = f2 + file_name
                        shutil.move(source, destination)

                    # for entity in entities:
                    #     if entity in oo2.keys():
                    #         values = oo2.get(entity)
                    #         if (entity.replace(" ", "_").lower() in databaseattribute.keys()):
                    #             databaseattribute.update(
                    #                 {entity.replace(" ", "_").lower(): values})

                    # # print(databaseattribute)
                    # for key, values in databaseattribute.items():
                    #     if (databaseattribute[key] == None):
                    #         databaseattribute[key] = 'Null'

                    # cur.execute("INSERT INTO model(unknown,name,degree,skills,college_name,university,graduation_year,companies_worked_at,designation,years_of_experience,location,address,rewards_achievements,projects) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    #             (databasevalue(databaseattribute.get('unknown')), databasevalue(databaseattribute.get('name')), databasevalue(databaseattribute.get('degree')), databasevalue(databaseattribute.get('skills')), databasevalue(databaseattribute.get('college_name')), databasevalue(databaseattribute.get('university')), databasevalue(databaseattribute.get('graduation_year')), databasevalue(databaseattribute.get('companies_worked_at')), databasevalue(databaseattribute.get('designation')), databasevalue(databaseattribute.get('years_of_experience')), databasevalue(databaseattribute.get('location')), databasevalue(databaseattribute.get('address')), databasevalue(databaseattribute.get('rewards_achievements')), databasevalue(databaseattribute.get('projects')),))

                    # cur.execute(
                    #     "INSERT INTO list(email) VALUES (%s)", (mailid,))

                    # for key, values in databaseattribute.items():
                    #     databaseattribute[key] = 'Null'

                else:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                    # inserting path to save the file *********************************************************
                    binary = f2 + filename
                    x = binary.rindex(index)
                    y = binary.rindex(".")

                    num = str(val)
                    val = val+1

                    path = binary[:x + 1] + "resume" + num + binary[y:]
                    filerename = "resume" + num + binary[y:]
                    os.rename(binary, path)
                    binartfile = convertToBinary(path)

                    cur.execute(
                        "INSERT INTO deepbluecomp_table(files_path,binaryfiles_path) VALUES (%s, %s)", (filerename, binartfile))
                    print(path)
                    mysql.connection.commit()

                    # add to database
                    text1, link, mailid, ftext = fileconversion0000(
                            path, num)
                    linkdedln, github, others = get_links(link)

                    cur.execute(
                            "INSERT INTO parse( extracted_text, cleaned_text,emails, linkedin_link, github_link,extra_link) VALUES (%s, %s, %s, %s, %s, %s )",
                            (text1, ftext, mailid, linkdedln, github, others,))

                    mysql.connection.commit()
                    print("\n------MODELS--------\n")
                    outparsed = parser(path)
                    print("out:",outparsed)
                    cur.execute(
                            "INSERT INTO modelfinal( Name, Phone_Number,Email_id,Gender, DOB,Location,Pincode,Current_Job,TExperience,Designation,Company,Experience_Year,Projects,Degrees,College,YearOfPassout,Courses,Publication,Skills,Referr,Awards,University,Degree,CompaniesWorkedat) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,%s,%s, %s, %s,%s)",
                            ((personal1(outparsed.get('Personal Details')),) ,(personal2(outparsed.get('Personal Details')),) ,(personal3(outparsed.get('Personal Details')),), (personal4(outparsed.get('Personal Details')),), (personal5(outparsed.get('Personal Details')),) ,(personal6(outparsed.get('Personal Details')),),(personal7(outparsed.get('Personal Details'))) ,(cjob(outparsed),),(totalexp(outparsed),) ,(experdetails1(outparsed.get('Experience')),),(experdetails2(outparsed.get('Experience')),) ,(experdetails3(outparsed.get('Experience')),) ,(experdetails4(outparsed.get('Experience')),),(edudetails1(outparsed.get('Education')),) ,(edudetails2(outparsed.get('Education')),),(edudetails3(outparsed.get('Education')),),(edudetails4(outparsed.get('Education')),) ,(edudetails5(outparsed.get('Education')),) ,(skilldetails(outparsed.get('Skills')),),(refdetails(outparsed.get('Reference')),),(award(outparsed.get('Awards')),),(university(outparsed.get('university')),),(degrees(outparsed.get('degree')),),(cwat(outparsed.get('Companies worked at')),)   ,))
                    mysql.connection.commit()
                    
                    
                    
                    


    mysql.connection.commit()
    cur.close()
    flash('File(s) successfully uploaded')
    table_li = []

    cur = mysql.connection.cursor()
    result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM modelfinal')
    # name,education,skills,experience,email
    if result > 0:
        row = cur.fetchall()
        for dict in row:
            table_li.append(list(dict.values()))

    # return redirect('/upload')
    return render_template('table2.html', row=table_li)
    
    # # return redirect('/upload')
    # table_li = []

    # cur = mysql.connection.cursor()
    # result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM model')
    # # name,education,skills,experience,email
    # print(result)
    # if result > 0:
    #     row = cur.fetchall()
    #     print(row)
    #     for dict in row:
    #         table_li.append(list(dict.values()))
    #     print(table_li)

    # # return redirect('/upload')
    # return render_template('table2.html', row=table_li)


@app.route("/delete")
def delete():
    dirzip_list = os.listdir(app.config['ZIPPED'])

    for zipfileli in dirzip_list:
        os.remove(z2 + zipfileli)

    dirrar_list = os.listdir(app.config['EXTRACTED'])

    for rarfileli in dirrar_list:
        os.remove(e2 + rarfileli)

    folder = f2
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return render_template('upload2.html')

#table 2 page
@app.route('/table', methods=["POST", "GET"])
def table():
    table_li = []

    cur = mysql.connection.cursor()
    result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM modelfinal')
    # name,education,skills,experience,email
    if result > 0:
        row = cur.fetchall()
        for dict in row:
            table_li.append(list(dict.values()))


    return render_template('table2.html', row=table_li)


#compare
@app.route('/compare', methods=["POST", "GET"])
def compare():
    table_data = []
    if request.method == "POST":
        candiatecomparelist = request.form.getlist('check')
        cur = mysql.connection.cursor()
        for i in candiatecomparelist:
            compresult = cur.execute(
                "Select can_id,Name,Degrees,Skills,Experience_Year,Email_id,CompaniesWorkedat,Projects from modelfinal WHERE can_id= %s ", (int(i),))
            print(compresult)
            if compresult > 0:
                row = cur.fetchall()
                print(row)
                for dict in row:
                    table_data.append(list(dict.values()))
                print(table_data)

    return render_template('compare.html', cont=table_data)

#statics table page
@app.route('/statistic', methods=["POST", "GET"])
def statistic():
    return render_template('statistic.html')


#summary page
@app.route('/summary/<int:project_id>', methods=["POST", "GET"])
def summary(project_id):
    print(project_id)
    table_data = []
    linked_list = []
    git_list=[]
    summarry_list=[]


    cur = mysql.connection.cursor()

    compresult = cur.execute("Select * from modelfinal WHERE can_id= %s ",
                                     (int(project_id),))
    if compresult > 0:
        row = cur.fetchall()
        print("row ,",row)
        for dict in row:
            table_data.append(list(dict.values()))
        print(table_data)

    linkedln_details_no = cur.execute("Select Education_l,Expirence_l,Licenses_Certificates_l,Skills_l,Projects_l,Honors_awards_l,Languages_l,About_l,Activity_l,Interest,Causes_l,Featured_l,Volunteering from linkdien WHERE can_id= %s ",
                             (int(project_id),))
    if linkedln_details_no > 0:
        linkedln_details = cur.fetchall()
        print("row ,", linkedln_details)
        for dict in linkedln_details:
            linked_list.append(list(dict.values()))
        print(linked_list)


    gitresult = cur.execute("Select GithubProjects from linkdien WHERE can_id= %s ",
                             (int(project_id),))
    if gitresult > 0:
        row2 = cur.fetchall()
        print("row ,", row2)
        for dict in row2:
            git_list.append(list(dict.values()))
        print(git_list)

    summaryresult = cur.execute("Select summary_A from linkdien WHERE can_id= %s ",
                           (int(project_id),))
    if summaryresult > 0:
        row2 = cur.fetchall()
        print("row ,", row2)
        for dict in row2:
            summarry_list.append(list(dict.values()))
        print(summarry_list)

    return render_template('summarypage.html', cont=table_data , lindata=linked_list,gitdata=git_list,summary=summarry_list)

@app.route('/select',methods=["POST","GET"])
def select():
    selectcolumn1=[]
    if request.method == "POST":
        selectedcolumn = request.form.getlist('selectedcolumn')
        print(selectedcolumn)
        columnname = " , ".join(map(str, selectedcolumn))
        print(columnname)
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT can_id, '+str(columnname) +' FROM modelfinal')
        # cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM model')
        # name,education,skills,experience,email
        if result > 0:
            row = cur.fetchall()
            for dict in row:
                selectcolumn1.append(list(dict.values()))
            print(selectedcolumn)

    return render_template('selecttable.html',column=selectedcolumn,rowdata=selectcolumn1)


#files
@app.route('/show/<int:can_id>', methods=["POST", "GET"])
def show(can_id):
    print(can_id)
    resume_path = []
    cur = mysql.connection.cursor()

    compresult = cur.execute("Select files_path from deepbluecomp_table WHERE sr= %s ",
                             (int(can_id),))
    if compresult > 0:
        row = cur.fetchall()
        print("row ,", row)
        for dict in row:
            resume_path.append(list(dict.values()))
        print(resume_path[0][0])

    return send_from_directory(UPLOAD_FOLDER,resume_path[0][0])


#setting
@app.route('/setting', methods=["POST", "GET"])
def setting():

    return render_template('setting.html')

#table3
@app.route('/table3', methods=["POST", "GET"])
def table3():
    table_li = []
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM modelfinal')
    # name,education,skills,experience,email
    if result > 0:
        row = cur.fetchall()
        for dict in row:
            table_li.append(list(dict.values()))

    return render_template('table3.html', row=table_li)

#ranking
@app.route('/rank', methods=["POST", "GET"])
def rank():
    rank_li=[]
    if request.method == "POST":
        education = request.form.getlist('education')
        othereducation=request.form.get('others')
        jobdescription=request.form.get('jobtext')
        print(education, othereducation, jobdescription)
        cur = mysql.connection.cursor()

        result = cur.execute("Select can_id,cleaned_text from parse  ")
        if result>0:
            row = cur.fetchall()
            print("row ,", row)
            for data in row:

                rank = ranking(jobdescription,data.get('cleaned_text'))
                rank = int(rank)
                print(type(rank))
                print("rank : ",rank)
                cur.execute("UPDATE modelfinal SET Rank =%s WHERE can_id=%s",(rank,data.get('can_id')))
                # cur.execute(insertrank, (0.0, 1))
            mysql.connection.commit()
            # cur.close()
            cur = mysql.connection.cursor()
            result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Rank FROM modelfinal ORDER BY Rank DESC')
            # name,education,skills,experience,email
            if result > 0:
                row = cur.fetchall()
                for dict in row:
                    rank_li.append(list(dict.values()))



    return render_template('ranktable2.html',row=rank_li)


#linkdien route
@app.route('/linkedln',methods=["POST","GET"])
def linkdedln():
    # count=18
    cur = mysql.connection.cursor()
    # # while(count>=18):
    om = cur.execute("Select * from linkdien")
    mysql.connection.commit()
    if om==0:
        row = cur.execute("Select cleaned_text,linkedin_link,github_link from parse ")

        if row>0:
                linkedlnlink=cur.fetchall()
                # link=linkedlnlink[0].get('linkedin_link')
                print(linkedlnlink)
        count = 1
        
        for subdic in linkedlnlink:
            link = ''
            cleaneddata=""
            cleaneddata=subdic.get('cleaned_text')
            link=subdic.get('linkedin_link')
            github=subdic.get('github_link')
            print(count)


            #link=link.replace(',','')
            if(link=='' and github==''):
                        summary1= summary_model(cleaneddata,model_summary)
                        print(summary1)
                        cur.execute("INSERT INTO linkdien(Education_l,summary_A,GithubProjects) VALUES (%s,%s,%s)",("Link Not Found",summary1,"Link Not Found",))
                        mysql.connection.commit()
            else:
                        # try:
                            emptyB()
                            emptyBClean()
                            flink=link.replace(',','')
                            # cur.execute("UPDATE parse SET webscraplinkedln =%s WHERE can_id=%s", (linked_in_scrap(flink), count))

                            linked_data=linked_in_scrap(flink)
                            
                            print("data : ",linked_data)
                            summary1= summary_model(cleaneddata,model_summary)
                            print(summary1)

                            cur.execute("INSERT INTO linkdien(Education_l ,Expirence_l ,Licenses_Certificates_l ,Skills_l,Projects_l,Honors_awards_l,Languages_l,About_l,Activity_l,Interest,Causes_l,Featured_l,Volunteering,summary_A) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (linkedlndb(linked_data.get('Education')), linkedlndb(linked_data.get('Experience')), linkedlndb(linked_data.get('Licenses & certifications')),linkedlndb(linked_data.get('Skills')),linkedlndb(linked_data.get('Projects')),linkedlndb(linked_data.get('Honors & awards')),linkedlndb(linked_data.get('Languages')),linkedlndb(linked_data.get('About')),linkedlndb(linked_data.get('Activity')),linkedlndb(linked_data.get('Interests')),linkedlndb(linked_data.get('Causes')),linkedlndb(linked_data.get('Featured')),linkedlndb(linked_data.get('Volunteering')),summary1,))
                            mysql.connection.commit()
                        # except:
                        #     cur.execute("INSERT INTO linkdien(Education_l) VALUES (%s)", ("Technical issue"))


            count = count + 1
            mysql.connection.commit()
        table_li = []
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM modelfinal')
        # name,education,skills,experience,email
        if result > 0:
            row = cur.fetchall()
            for dict in row:
                table_li.append(list(dict.values()))

        # return redirect('/upload')
        return render_template('table3.html', row=table_li)
    else:
        table_li = []
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT can_id,Name,Degrees,Skills,TExperience,Email_id FROM modelfinal')
        # name,education,skills,experience,email
        if result > 0:
            row = cur.fetchall()
            for dict in row:
                table_li.append(list(dict.values()))
        return render_template('table3.html', row=table_li)



if __name__ == "__main__":
    app.run()