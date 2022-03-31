from time import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import hashlib

def emptyB():
    for i in range(12):
        #print(i + 1)
        f = open('blocks/'+str(i + 1) + "b.txt", "w")
        f.write('')
        f.close()


def emptyBClean():
    for i in range(12):
        #print(i + 1)
        f = open('blocks/'+str(i + 1) + "bclean.txt", "w")
        f.write('')
        f.close()

def getAbout(soup):
    link_About = soup.find('div', {"class": "display-flex ph5 pv3"})
    about = ''
    for ab in link_About:
        about = ab.text
        print(ab.text)

    return about

def currentWork(soup):
    current_work = soup.find('div', {"class": "text-body-medium break-words"})
    for data in current_work:
        print(data.text)
        return data.text

def removeWords():
    bad_words = ['Message', 'logo', 'See credential', 'Expiration Date', 'followers', 'See all', '�', 'comments',
                 '.pdf']
    for i in range(12):
        with open(f'blocks/{str(i + 1)}bclean.txt', 'r', encoding='utf-8') as oldfile, open(f'blocks/{str(i + 1)}b.txt','w', encoding='utf-8') as newfile:
            for line in oldfile:
                if not any(bad_word in line for bad_word in bad_words):
                    newfile.write(line)


def removeDupes():
    for i in range(12):
        inputFile = f'blocks/{str(i + 1)}b.txt'
        outputFile = f'blocks/{str(i + 1)}bclean.txt'
        completed_lines_hash = set()
        output_file = open(outputFile, "w", encoding='utf-8')
        for line in open(inputFile, "r", encoding='utf-8'):
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
            if hashValue not in completed_lines_hash:
                output_file.write(line)
                completed_lines_hash.add(hashValue)
        output_file.close()


def linked_in_scrap(LINK):

    emptyB()
    emptyBClean()

    # PATH to chrome driver
    AD_CHROME_PATH = '/Users/cosmos/chromedriver'
    ser = Service(AD_CHROME_PATH)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)

    # USERNAME AND PASSWORD
    USERNAME = 'omsurve570@gmail.com'
    PASSWORD = 'lucario123'

    # open linkedin.com
    driver.get("https://www.linkedin.com/login")
    driver.implicitly_wait(2)

    # get Username , Password tag and send details and Hit Enter
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # GOTO REQUIRED PERSON PROFILE
    driver.get(LINK)

    pagesource = driver.page_source
    soup = BeautifulSoup(pagesource, "html.parser").encode("utf-8")

    firstBox = ''
    secondBox = ''
    thirdBox = ''
    fourthBox = ''
    fifthBox = ''
    sixthBox = ''
    seventhBox = ''
    eighthBox = ''
    ninthBox = ''
    tenthBox = ''
    eleventhBox = ''
    twelvethBox = ''

    try:
        firstBox = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[2]').text
        secondBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[3]').text
        thirdBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[4]').text
        fourthBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[5]').text
        fifthBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[6]').text
        sixthBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[7]').text
        seventhBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[8]').text
        eighthBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[9]').text
        ninthBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[10]').text
        tenthBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[11]').text
        eleventhBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[12]').text
        twelvethBox = driver.find_element_by_xpath(
            '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[13]').text


    except:
        print('error')

    finally:
        print('First Box :' + firstBox)
        f = open("blocks/1b.txt", "a", encoding="utf-8")
        f.write(firstBox)
        f.close()

        print('Second Box :' + secondBox)
        f = open("blocks/2b.txt", "a", encoding="utf-8")
        f.write(secondBox)
        f.close()

        print('Third Box :' + thirdBox)
        f = open("blocks/3b.txt", "a", encoding="utf-8")
        f.write(thirdBox)
        f.close()

        print('Fourth Box :' + fourthBox)
        f = open("blocks/4b.txt", "a", encoding="utf-8")
        f.write(fourthBox)
        f.close()

        print('Fifth Box :' + fifthBox)
        f = open("blocks/5b.txt", "a", encoding="utf-8")
        f.write(fifthBox)
        f.close()

        print('Sixth Box :' + sixthBox)
        f = open("blocks/6b.txt", "a", encoding="utf-8")
        f.write(sixthBox)
        f.close()

        print('Seventh Box :' + seventhBox)
        f = open("blocks/7b.txt", "a", encoding="utf-8")
        f.write(seventhBox)
        f.close()

        print('Seventh Box :' + eighthBox)
        f = open("blocks/8b.txt", "a", encoding="utf-8")
        f.write(eighthBox)
        f.close()

        print('ninthBox Box :' + ninthBox)
        f = open("blocks/9b.txt", "a", encoding="utf-8")
        f.write(ninthBox)
        f.close()

        print('tenthBox Box :' + tenthBox)
        f = open("blocks/10b.txt", "a", encoding="utf-8")
        f.write(tenthBox)
        f.close()

        print('eleventhBox Box :' + eleventhBox)
        f = open("blocks/11b.txt", "a", encoding="utf-8")
        f.write(eleventhBox)
        f.close()

        print('twelvethBox Box :' + twelvethBox)
        f = open("blocks/12b.txt", "a", encoding="utf-8")
        f.write(twelvethBox)
        f.close()

        removeDupes()
        removeWords()

        elements = ['Highlights', 'About', 'Activity', 'Education', 'Experience', 'Licenses & certifications', 'Skills',
                    'Projects', 'Honors & awards', 'Languages', 'Interests', 'Causes', 'Featured']

        my_dict = {}
        for i in range(14):
            with open(f"blocks/{i + 1}b.txt", "r", encoding='utf-8') as file:
                first_line = file.readline()
                for j in range(13):
                    if elements[j] in first_line:
                        remaining_lines = file.readlines()
                        my_dict[elements[i]] = remaining_lines
                        break
                    else:
                        j += 1

        print(my_dict)

        driver.quit()
        return my_dict



# emptyB()
# emptyBClean()
# linked_in_scrap(link)
# github_scrape(link)
