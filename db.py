from preprocessing import * #url_func,email,get_phone_numbers,data_grabber,address_grabber,pincode_grabber,get_human_names,pre_process1_rsw1,remove_hexcode_rhc


def databasevalue(listofvalues):
    insertdata=""
    if(listofvalues=='Null'):
        return 'Null'
    else:
        for value in listofvalues:
            insertdata=insertdata+value +","

        return insertdata


def givedata(text):
    scraplink = ""
    eid = ""
    phno = ""
    f_human_name = ""
    fdate = ""
    address = ""

    link = url_func(text)
    if (len(link) == 0):
        scraplink = "null"
    else:
        scraplink = ""
        for i in link:
            scraplink = scraplink + "  " + i

    mailid = email(text)
    mailid=set(mailid)
    for i in mailid:
        eid = i + "  " + eid
    if (eid is None):
        eid = "null"

    phone_number = get_phone_numbers(text)
    #phone_number = phone_number[len(phone_number0) -1]
    if (len(phone_number) == 0):
        phno = "null"
    else:
        for i in phone_number:
            phno = i + "  " + phno

    e_date = data_grabber(text)
    if (len(e_date) == 0):
        fdate = "null"
    else:
        for k in e_date:
            fdate = fdate + "  " + str(k)

    human_name = get_human_names(text)
    if (human_name is None):
        f_human_name = "null"
    else:
        for i in human_name:
            f_human_name = f_human_name + " " + i

    add = address_grabber(text)
    if (len(add) == 0):
        address = "null"
    else:
        for ad in add:
            address = address + "  " + ad
    
    # try:

    pincode = pincode_grabber(text)
    print("fileconversion : ",text)
    text1 = pre_process1_rsw1(text)
    ftext = remove_hexcode_rhc(text1)
    # except:
    #     pincode = "NAN"
    #     text1= "NAN"
    #     ftext = "NAN"
        
    return (text, text1, scraplink, eid, phno, fdate, f_human_name, address, pincode, ftext)