def linkedlndb(value):
  try:
    if(len(value)==0):
        return 'null'
    else:
        str1 = " , ".join(map(str,value))
        return (str(str1))
  except:
    return 'null'