def personal1(details):

    return (details.get('Name'))
def personal2(details):
    if(len(details.get('Phone Number'))==0):
        return 'null'
    else:
        str1 = " "
    return (str1.join(details.get('Phone Number')))

def personal3(details):
    if(details.get('Email Id')==''):
        return 'null'
    else:
        return (details.get('Email Id'))

def personal4(details):
    return details.get('Gender')

def personal5(details):
    if(details.get('Date of birth')==''):
        return 'null'
    else:
         return (details.get('Date of birth'))

def personal6(details):
    return (details.get('Location'))

def personal6(details):
    if(details.get('Pincode')=='' or details.get('Pincode')==' '):
        return 'null'
    else:
        return (details.get('Pincode'))

def cjob(data):
    if(data.get('Current Job')==''):
        return 'null'
    else:
        return (data.get('Current Job'))
def experdetails1(edetails):
    if(len(edetails.get('Designation'))== 0):
        return 'null'
    else:
        str2 = " "
        return (str2.join(edetails.get('Designation')))
def experdetails2(edetails):
    if(len(edetails.get('Company'))==0):
        return 'null'
    else:
        str3 = " "
        return (str3.join(edetails.get('Company')))

def experdetails3(edetails):
    if(len(edetails.get('Experience Year'))==0):
        return 'null'
    else:
        str4="   "
        return (str4.join(edetails.get('Experience Year')))

def experdetails4(edetails):
    if(edetails.get('Projects')==''):
        return 'null'
    else:
        return (edetails.get('Projects'))

def edudetails1(edudetails):
    if(len(edudetails.get('Degree'))==0):
        return'null'
    else:
        str5 = " "
        return (str5.join(edudetails.get('Degree')))

def edudetails2(edudetails):
    if(len(edudetails.get('College'))==0):
        return'null'
    else:
        str6 = " "
        return (str6.join(edudetails.get('College')))

def edudetails3(edudetails):
    if (len(edudetails.get('Graduation Year')) == 0):
        return 'null'
    else:
        str7 = " "
        return (str7.join(edudetails.get('Graduation Year')))

def edudetails4(edudetails):
    if(edudetails.get('Trainings/Courses')==''):
        return 'null'
    else:
        return (edudetails.get('Trainings/Courses'))


def edudetails5(edudetails):
    if (edudetails.get('Publications') == ''):
        return 'null'
    else:
        return (edudetails.get('Publications'))

def skilldetails(skills):
    if (len(skills) == 0):
        return 'null'
    else:
        str7 = ", "
        return (str7.join(skills))

def refdetails(refdetails):
    if (len(refdetails) == 0):
        return 'null'
    else:
        str7 = " "
        return (str7.join(refdetails))

def award(awards):
    if(awards==''):
        return 'null'
    else:
        return awards


def university(university):
    if (len(university) == 0):
        return 'null'
    else:
        str8 = " "
        return (str8.join(university))


def degrees(degree):
    if(len(degree)==0):
        return 'null'
    else:
        str9 = " "
        return (str9.join(degree))


def cwat(workedat):
    if(len(workedat)==0):
        return 'null'
    else:
        str10 = " "
        return (str10.join(workedat))


print(skilldetails( ['Instrumentation', 'Communication', 'Commissioning', 'Electronics', 'Programming', 'Electrical', 'Automation', 'Analytical', 'Training', 'Autocad', 'English', 'Matlab', 'Mobile', 'System']))

print( personal2( {'Name': 'None', 'Phone Number': ['+91)7503729071'], 'Email Id': 'salman.ali19@gmail.com', 'Gender': 'not mentioned', 'Date of birth': '', 'Location': 'Null', 'Pincode': ' '}))
