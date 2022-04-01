from constants import *
from ast import Return
from flask import Flask, render_template, request, flash, redirect
from flask import *
import os
import shutil
import pymysql
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

from fileconversion import fileconversion1
from preprocessing import*
from preprocessing import dict_clean
from linkedIn import linked_in_scrap
from githubs import github_scrape
from model import*
from db import *
from config import *
from flask_fun import * 
from constants import *




# BERT

#STATE_DICT = torch.load(bert_dict_path, map_location=DEVICE)
#TOKENIZER = BertTokenizerFast.from_pretrained(MODEL_PATH, lowercase=True)
#TOKENIZER = Tokenizer(num_words=20000)  # SIMPLE
# MODEL = BertForTokenClassification.from_pretrained(
#    MODEL_PATH, state_dict=STATE_DICT['model_state_dict'], num_labels=12)
# model = MODEL
# MODEL.to(DEVICE);
print('\nModel Loaded!\n')

# model_summary = SimpleT5()
# model_summary.from_pretrained(model_type="t5", model_name="t5-large")
# model_summary.load_model(summary_model, use_gpu=False)

# tokenizer_bert_ner = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model_bert_ner = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
print('\n NER Model & Summary Loaded!\n')

# flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
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
                        original = e2 + \
                            str(i)
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
                        print("------")
                        text, text1, link, mailid, phone_number, date, human_name, add, pincode, ftext = fileconversion1(
                            path, num)
                        linkdedln, github, others = get_links(link)

                        cur.execute(
                            "INSERT INTO parse( extracted_text, cleaned_text,state, emails, linkedin_link, github_link,extra_link,phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )",
                            (text1, ftext, pincode, mailid, linkdedln, github, others, phone_number))

                    dir_list = os.listdir(app.config['EXTRACTED'])
                    for file_name in dir_list:
                        source = e2 + file_name
                        destination = f2 + file_name
                        shutil.move(source, destination)

                    oo2 = spacy_700(text2)

                    for entity in entities:
                        if entity in oo2.keys():
                            values = oo2.get(entity)
                            if (entity.replace(" ", "_").lower() in databaseattribute.keys()):
                                databaseattribute.update(
                                    {entity.replace(" ", "_").lower(): values})

                    # print(databaseattribute)
                    for key, values in databaseattribute.items():
                        if (databaseattribute[key] == None):
                            databaseattribute[key] = 'Null'

                    cur.execute("INSERT INTO model(unknown,name,degree,skills,college_name,university,graduation_year,companies_worked_at,designation,years_of_experience,location,address,rewards_achievements,projects) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (databasevalue(databaseattribute.get('unknown')), databasevalue(databaseattribute.get('name')), databasevalue(databaseattribute.get('degree')), databasevalue(databaseattribute.get('skills')), databasevalue(databaseattribute.get('college_name')), databasevalue(databaseattribute.get('university')), databasevalue(databaseattribute.get('graduation_year')), databasevalue(databaseattribute.get('companies_worked_at')), databasevalue(databaseattribute.get('designation')), databasevalue(databaseattribute.get('years_of_experience')), databasevalue(databaseattribute.get('location')), databasevalue(databaseattribute.get('address')), databasevalue(databaseattribute.get('rewards_achievements')), databasevalue(databaseattribute.get('projects')),))

                    cur.execute(
                        "INSERT INTO list(email) VALUES (%s)", (mailid,))

                    for key, values in databaseattribute.items():
                        databaseattribute[key] = 'Null'

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
                        original = e2 + \
                            str(i)
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
                        text, text1, link, mailid, phone_number, date, human_name, add, pincode, ftext = fileconversion1(
                            path, num)
                        linkdedln, github, others = get_links(link)

                        cur.execute(
                            "INSERT INTO parse( extracted_text, cleaned_text,state, emails, linkedin_link, github_link,extra_link,phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )",
                            (text1, ftext, pincode, mailid, linkdedln, github, others, phone_number))
                        # moving on to final folder
                    dir_list = os.listdir(app.config['EXTRACTED'])
                    for file_name in dir_list:
                        source = e2 + file_name
                        destination = f2+ file_name
                        shutil.move(source, destination)

                    #oo2 = spacy_700(text2)

                    for entity in entities:
                        if entity in oo2.keys():
                            values = oo2.get(entity)
                            if (entity.replace(" ", "_").lower() in databaseattribute.keys()):
                                databaseattribute.update(
                                    {entity.replace(" ", "_").lower(): values})

                    # print(databaseattribute)
                    for key, values in databaseattribute.items():
                        if (databaseattribute[key] == None):
                            databaseattribute[key] = 'Null'

                    cur.execute("INSERT INTO model(unknown,name,degree,skills,college_name,university,graduation_year,companies_worked_at,designation,years_of_experience,location,address,rewards_achievements,projects) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (databasevalue(databaseattribute.get('unknown')), databasevalue(databaseattribute.get('name')), databasevalue(databaseattribute.get('degree')), databasevalue(databaseattribute.get('skills')), databasevalue(databaseattribute.get('college_name')), databasevalue(databaseattribute.get('university')), databasevalue(databaseattribute.get('graduation_year')), databasevalue(databaseattribute.get('companies_worked_at')), databasevalue(databaseattribute.get('designation')), databasevalue(databaseattribute.get('years_of_experience')), databasevalue(databaseattribute.get('location')), databasevalue(databaseattribute.get('address')), databasevalue(databaseattribute.get('rewards_achievements')), databasevalue(databaseattribute.get('projects')),))

                    cur.execute(
                        "INSERT INTO list(email) VALUES (%s)", (mailid,))

                    for key, values in databaseattribute.items():
                        databaseattribute[key] = 'Null'

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
                    #binary = "C:\\Users\\Yash\\PycharmProjects\\flask\\static\\files\\"+filename
                    binartfile = convertToBinary(path)

                    cur.execute(
                        "INSERT INTO deepbluecomp_table(files_path,binaryfiles_path) VALUES (%s, %s)", (filerename, binartfile))
                    print(path)

                    text2, text1, link, mailid, phone_number, date, human_name, add, pincode, ftext = fileconversion1(
                        path, num)
                    linkdedln, github, others = get_links(link)
                    # add to database
                    cur.execute(
                        "INSERT INTO parse( extracted_text, cleaned_text,state, emails, linkedin_link, github_link,extra_link,phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )",
                        (text2, ftext, pincode, mailid, linkdedln, github, others, phone_number))

                    print("\n------MODELS--------\n")
                    print('------SPACY--------')
                    #oo1 = spacy_700(text1)
                    oo2 = spacy_700(text2)

                    for entity in entities:
                        if entity in oo2.keys():
                            values = oo2.get(entity)
                            if (entity.replace(" ", "_").lower() in databaseattribute.keys()):
                                databaseattribute.update(
                                    {entity.replace(" ", "_").lower(): values})

                    # print(databaseattribute)
                    for key, values in databaseattribute.items():
                        if (databaseattribute[key] == None):
                            databaseattribute[key] = 'Null'

                    cur.execute("INSERT INTO model(unknown,name,degree,skills,college_name,university,graduation_year,companies_worked_at,designation,years_of_experience,location,address,rewards_achievements,projects) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (databasevalue(databaseattribute.get('unknown')), databasevalue(databaseattribute.get('name')), databasevalue(databaseattribute.get('degree')), databasevalue(databaseattribute.get('skills')), databasevalue(databaseattribute.get('college_name')), databasevalue(databaseattribute.get('university')), databasevalue(databaseattribute.get('graduation_year')), databasevalue(databaseattribute.get('companies_worked_at')), databasevalue(databaseattribute.get('designation')), databasevalue(databaseattribute.get('years_of_experience')), databasevalue(databaseattribute.get('location')), databasevalue(databaseattribute.get('address')), databasevalue(databaseattribute.get('rewards_achievements')), databasevalue(databaseattribute.get('projects')),))

                    cur.execute(
                        "INSERT INTO list(email) VALUES (%s)", (mailid,))

                    for key, values in databaseattribute.items():
                        databaseattribute[key] = 'Null'

                    oo3 = spacy_700(ftext)
                    # oo2 = spacy_skills(text1)
                    # oo3 = spacy_edu(text1)
                    # oo4 = spacy_exp(text1)
                    # print(oo1)
                    print(oo3)
                    # print(oo3)
                    # print(oo4)
                    #entities1 = predict(MODEL, TOKENIZER, idx2tag, tag2idx, DEVICE, text1)
                    #output_bert = clean_bert(entities1, tags_vals)
                    # print(output_bert)
                    # print("------BERT--------")
                    # entities1 = predict(MODEL, TOKENIZER, idx2tag, tag2idx, DEVICE, text1)
                    # output_bert = clean_bert(entities1, tags_vals)
                    # print(output_bert)
                    print("------NAME--------")
                    # name_extracted = ner(text2,model_bert_ner,tokenizer_bert_ner) #is a list
                    # print(name_extracted)

                    # Linkdien
                    # if linkdedln != None:
                    #     if mailid or pincode is not None: #add here
                    #         linkdien_data = linkedien_scrape(linkdedln[0])
                    #         print(linkdien_data)

    mysql.connection.commit()
    cur.close()
    flash('File(s) successfully uploaded')
    # return redirect('/upload')
    table_li = []

    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM list')
    # name,education,skills,experience,email
    print(result)
    if result > 0:
        row = cur.fetchall()
        print(row)
        for dict in row:
            table_li.append(list(dict.values()))
        print(table_li)

    # return redirect('/upload')
    return render_template('table2.html', row=table_li)


@app.route("/delete")
def delete():
    dirzip_list = os.listdir(app.config['ZIPPED'])

    for zipfileli in dirzip_list:
        try:
            os.remove(z2 + zipfileli)
        except:
            print("Cannot delete")

    dirrar_list = os.listdir(app.config['EXTRACTED'])

    for rarfileli in dirrar_list:
        os.remove(f2 + rarfileli)

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


@app.route('/table', methods=["POST", "GET"])
def table():
    table_li = []

    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM list')
    # name,education,skills,experience,email
    if result > 0:
        row = cur.fetchall()
        for dict in row:
            table_li.append(list(dict.values()))

    return render_template('table2.html', row=table_li)


@app.route('/compare', methods=["POST", "GET"])
def compare():
    table_data = []
    if request.method == "POST":
        candiatecomparelist = request.form.getlist('check')
        cur = mysql.connection.cursor()
        for i in candiatecomparelist:
            compresult = cur.execute(
                "Select linked_link,github_link,extra_link from datastore WHERE sr= %s ", (int(i),))
            print(compresult)
            if compresult > 0:
                row = cur.fetchall()
                print(row)
                for dict in row:
                    table_data.append(list(dict.values()))
                print(table_data)

    return render_template('compare.html', cont=table_data)


@app.route('/statistic', methods=["POST", "GET"])
def statistic():
    return render_template('statistic.html')


if __name__ == "__main__":
    app.run(debug=True)
