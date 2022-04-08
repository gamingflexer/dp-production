from docx2pdf import convert
import cv2
from fpdf import FPDF
from PIL import Image
import pdfkit
import textract
import pytesseract
from tika import parser
from db import givedata
from autocorrect import Speller
from preprocessing import *

spell = Speller(only_replacements=True)

def fileconversion0000(filename, y):
    eid=""
    phno=""
    f_human_name=""
    fdate=""
    address=""
    scraplink = ""
    # count=1
    f_human_name=""
    pincode=""
    ftext=""
    x = filename.rfind(".")
    extension = filename[x + 1:]
    if (extension == "docx"):
      try:
        raw = parser.from_file(filename)
        text = raw['content']
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)

      except:
          try:
             text = textract.process(filename)
             text = text.replace("\n", " ")
             text = text.replace("\t", " ")
             text = spell(text)
             text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
          except:
              try:
                  text = textract.process(filename)
                  text = text.decode('utf-8')
                  text = text.replace("\n", " ")
                  text = text.replace("\t", " ")
                  text = spell(text)
                  text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
              except:
                  text = "Text Not Extracted"
                  text1 = "NAN"
                  scraplink = "NAN"
                  eid = "NAN"
                  phno = "NAN"
                  fdate = "NAN"
                  f_human_name = "NAN"
                  address = "NAN"
                  pincode = "NAN"
                  ftext = "NAN"


      print(text)
      text = text.replace("\n", " ")
      text = text.replace("\t", " ")
      print(text)

      return (text,scraplink, eid, ftext)

    elif (extension == "png" or extension == "jpg" or extension=="jpeg"):
      try:
          file = open(filename, "w")
          pdf = FPDF()
          pdf.add_page()
          fpdf = FPDF('L', 'cm', (500, 550))
          pdf.set_font("Arial", size=12)
          pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
          img = cv2.imread(filename)

          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # print(pytesseract.image_to_string(img))

          file.write(pytesseract.image_to_string(img))

          cv2.imshow('Result', img)

          file.close()
          f = open(filename, 'r')
          name1 = "D:\\deepbluefiles\\" + "resume" + y + ".pdf"
          for x in f:
            x = x.replace("\n", " ")
            x = x.replace("\t", " ")
            pdf.cell(200, 10, txt=x, ln=1, align='L')

          pdf.output(name1)
          raw = parser.from_file(filename)
          text = raw['content']
          text = spell(text)
          text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
      except:
          try:
              text = textract.process(filename)
              text = text.decode('utf-8')
              text = text.replace("\n", " ")
              text = text.replace("\t", " ")
              text = spell(text)
              text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
          except:
              try:
                  text = textract.process(filename)
                  text = text.decode('utf-8')
                  text = text.replace("\n", " ")
                  text = text.replace("\t", " ")
                  text = spell(text)
                  text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
              except:
                  text = "Text Not Extracted"
                  text1 = "NAN"
                  scraplink = "NAN"
                  eid = "NAN"
                  phno = "NAN"
                  fdate = "NAN"
                  f_human_name = "NAN"
                  address = "NAN"
                  pincode = "NAN"
                  ftext = "NAN"

      # text = textract.process(filename)

      return (text,scraplink, eid, ftext)

        #cursor.execute("INSERT INTO datastore( data, link, emailid, phoneno, date, humaname, address, code, data_two) VALUES (%s, %s )",(text1, link, mailid, phone_number, date, human_name, add, pincode, ftext))
    #   cv2.waitKey(0)

    elif (extension == "txt"):
      try:
        pdf = FPDF()
        pdf.add_page()
        fpdf = FPDF('L', 'cm', (500, 550))
        pdf.set_font("Arial", size=11)
        f = open(filename, 'r')
        for x in f:
            pdf.cell(200, 10, txt=x, ln=1, align='L')

        pdf.output(filename)
        raw = parser.from_file(filename)
        text = raw['content']
        text = spell(text)
        text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
      except:
          try:
              text = textract.process(filename)
              text = text.replace("\n", " ")
              text = text.replace("\t", " ")
              text = spell(text)
              text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
          except:
              try:
                  text = textract.process(filename)
                  text = text.decode('utf-8')
                  text = text.replace("\n", " ")
                  text = text.replace("\t", " ")
                  text = spell(text)
                  text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
              except:
                  text = "Text Not Extracted"
                  text1 = "NAN"
                  scraplink = "NAN"
                  eid = "NAN"
                  phno = "NAN"
                  fdate = "NAN"
                  f_human_name = "NAN"
                  address = "NAN"
                  pincode = "NAN"
                  ftext = "NAN"
      return (text,scraplink, eid, ftext)

    elif (extension == "html"):
       try:
        converted = "resume" + y + ".pdf"
        name = "D:\\deepbluefiles\\" + converted
        with open(filename) as f:
            pdfkit.from_file(f, filename)
        raw = parser.from_file(name)
        text = raw['content']
        text = spell(text)
        text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
       except:
           try:
               text = textract.process(filename)
               text = text.replace("\n", " ")
               text = text.replace("\t", " ")
               text = spell(text)
               text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
           except:
               try:
                   text = textract.process(filename)
                   text = text.decode('utf-8')
                   text = text.replace("\n", " ")
                   text = text.replace("\t", " ")
                   text = spell(text)
                   text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
               except:
                   text = "Text Not Extracted"
                   text1 = "NAN"
                   scraplink = "NAN"
                   eid = "NAN"
                   phno = "NAN"
                   fdate = "NAN"
                   f_human_name = "NAN"
                   address = "NAN"
                   pincode = "NAN"
                   ftext = "NAN"

       return (text,scraplink, eid, ftext)



    elif (extension == "rtf"):
        try:
            raw = parser.from_file(filename)
            text = raw['content']
            text = spell(text)
            text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
        except:
            try:
                raw = parser.from_file(filename)
                text = raw['content']
                text = text.decode('utf-8')
                text = spell(text)
                text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
            except:
                text = "Text Not Extracted"
                text1 = "NAN"
                scraplink = "NAN"
                eid = "NAN"
                phno = "NAN"
                fdate = "NAN"
                f_human_name = "NAN"
                address = "NAN"
                pincode = "NAN"
                ftext = "NAN"

        return (text,scraplink, eid, ftext)

    elif (extension == "odt"):
        try:
            raw = parser.from_file(filename)
            text = raw['content']
            text = spell(text)
            text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
        except:
            try:
                raw = parser.from_file(filename)
                text = raw['content']
                text = text.decode('utf-8')
                text = spell(text)
                text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
            except:
                text = "Text Not Extracted"
                text1 = "NAN"
                scraplink = "NAN"
                eid = "NAN"
                phno = "NAN"
                fdate = "NAN"
                f_human_name = "NAN"
                address = "NAN"
                pincode = "NAN"
                ftext = "NAN"

        return (text,scraplink, eid, ftext)

    elif (extension == "doc"):
        try:
            raw = parser.from_file(filename)
            text = raw['content']
            text = spell(text)
            text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
        except:
            try:
                raw = parser.from_file(filename)
                text = raw['content']
                text = text.decode('utf-8')
                text = spell(text)
                text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
            except:
                text = "Text Not Extracted"
                text1 = "NAN"
                scraplink = "NAN"
                eid = "NAN"
                phno = "NAN"
                fdate = "NAN"
                f_human_name = "NAN"
                address = "NAN"
                pincode = "NAN"
                ftext = "NAN"

        return (text,scraplink, eid, ftext)
    elif(extension == "pdf"):
        try:
            raw = parser.from_file(filename)
            text = raw['content']
            text = spell(text)
            print("under try1 text : ",text)
            text,text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext=givedata(text)
            print("underfile")

        except:
            # try:
                raw = parser.from_file(filename)
                text = raw['content']
                text = spell(text)
                print("under try2 text : ",text)
                text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext = givedata(text)
            # except:
                # text = "Text Not Extracted"
                # text1 = "NAN"
                # scraplink = "NAN"
                # eid = "NAN"
                # phno = "NAN"
                # fdate = "NAN"
                # f_human_name = "NAN"
                # address = "NAN"
                # pincode = "NAN"
                # ftext = "NAN"
                # print("under except")



    return text,scraplink, eid, ftext







