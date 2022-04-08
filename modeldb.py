def personal1(details):

    return (str(details.get('Name')))
def personal2(details):
    if(len(details.get('Phone Number'))==0):
        return 'null'
    else:
         str01 = " , ".join(map(str,details.get('Phone Number')))
    return (str01)

def personal3(details):
    if(details.get('Email Id')==''):
        return 'null'
    else:
        return (str(details.get('Email Id')))

def personal4(details):
    return details.get('Gender')

def personal5(details):
    if(details.get('Date of birth')==''):
        return 'null'
    else:
         return (str(details.get('Date of birth')))

def personal6(details):
    return (str(details.get('Location')))

def personal7(details):
    if(details.get('Pincode')=='' or details.get('Pincode')==' '):
        return 'null'
    else:
        return (str(details.get('Pincode')))

def cjob(data):
    if(data.get('Current Job')==''):
        print("cjob under null")
        return 'null'
    else:
      print("cjob",data.get('Current Job'))
      return (str(data.get('Current Job')))
def totalexp(data):
    if(data.get('Total Experience(years)')==''):
      print("Totalexp under null")
      return 'null'
    else:
        print("totalexp",data.get('Total Experience(years)'))
        return (str(data.get('Total Experience(years)')))        
def experdetails1(edetails):
    if(len(edetails.get('Designation'))== 0):
      print("exper1 under null")
      return 'null'
    else:
        print(edetails.get('Designation'))
        str1 = " , ".join(map(str,edetails.get('Designation')))
        print(str(str1))
        return (str(str1))

         
def experdetails2(edetails):
    if(len(edetails.get('Company'))==0):
      print("exper2 under null")
      return 'null'
    else:
      
        print(edetails)
        str2 = " , ".join(map(str,edetails.get('Company')))
        print(str(str2))
        return (str(str2))
          

def experdetails3(edetails):
    if(len(edetails.get('Experience Year'))==0):
      print("exper3 under null")
      return 'null'
    else:
     
        
        print(edetails)
        str3 = " , ".join(map(str,edetails.get('Experience Year')))
        print(str3)
        return (str(str3))
      

def experdetails4(edetails):
    if(edetails.get('Projects')==''):
      print("exper4 under null")
      return 'null'
    else:
      print(edetails.get('Projects'))
      return (str(edetails.get('Projects')))

def edudetails1(edudetails):
    if(len(edudetails.get('Degree'))==0):
      print("edu1 under null")
      return'null'
    else:

        str4 = " , ".join(map(str,edudetails.get('Degree')))
        print(str(str4))
        return (str(str4))

def edudetails2(edudetails):
    if(len(edudetails.get('College'))==0):
      print("edu2 under null")
      return'null'
    else:
        print(edudetails)
        
        str5 = " , ".join(map(str,edudetails.get('College')))
        print(str(str5))
        return (str(str5))

def edudetails3(edudetails):
    if (len(edudetails.get('Graduation Year')) == 0):
      print("edu3 under null")
      return 'null'
    else:
        print(edudetails)
        str6 = " , ".join(map(str,edudetails.get('Graduation Year')))
        print(str(str6))
        return (str(str6))

def edudetails4(edudetails):
    if(edudetails.get('Trainings/Courses')==''):
      print("edu4 under null")
      return 'null'
    else:
      print(edudetails.get('Trainings/Courses'))
      return (str(edudetails.get('Trainings/Courses')))
     
        


def edudetails5(edudetails):
    if (edudetails.get('Publications') == ''):
      print("edu5 under null")
      return 'null'
    else:
      print(edudetails.get('Publications'))
      return (str(edudetails.get('Publications')))
        

def skilldetails(skills):
    if (len(skills) == 0):
      print("skills under null")
      return 'null'
    else:
      print(skills)
      skills2 = set(skills)
      str7 = " , ".join(map(str,skills2))
      
      print(str(str7))

      return (str(str7))
      

def refdetails(refdetails):
    if (len(refdetails) == 0):
        print("under refer null")
        return 'null'
    else:
        print(refdetails)
        str8 = " , ".join(map(str,refdetails))
        print( "ref:",str(str8))

        return (str(str8)) 

def award(awards):
    if(awards==''):
      print("awards under null")
      return 'null'
    else:
      print(awards)
      return (str(awards)) 



def university(university):
    if (len(university) == 0):
        return 'null'
    else:

        print(university)
        str9 = " , ".join(map(str,university))
        print(str(str9))
        return (str(str9))
       


def degrees(degree):
    
    if(len(degree)==0):
      print("under degree null")
      return 'null'
    else:
      
        print(degree)
        str10 = " , ".join(map(str,degree))
        print(str(str10))
        return (str(str10))
       


def cwat(workedat):
    if(len(workedat)==0):
      print("under null")
      return 'null'
    else:
      
        
        str11 = " , ".join(map(str,workedat))
        print(str(str11))
        return (str(str11))
       


# print(skilldetails( ['Instrumentation', 'Communication', 'Commissioning', 'Electronics', 'Programming', 'Electrical', 'Automation', 'Analytical', 'Training', 'Autocad', 'English', 'Matlab', 'Mobile', 'System']))

# print( personal2( {'Name': 'None', 'Phone Number': ['+91)7503729071'], 'Email Id': 'salman.ali19@gmail.com', 'Gender': 'not mentioned', 'Date of birth': '', 'Location': 'Null', 'Pincode': ' '}))
