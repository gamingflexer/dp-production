import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def github_scrape(userURL):
    try:
        option = webdriver.ChromeOptions()
        bl = "/Users/cosmos/chromedriver"
        option.bl = bl
        driver = webdriver.Chrome(executable_path=r'/Users/cosmos/chromedriver', options=option)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        option.add_experimental_option("prefs", prefs)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        reposURL = userURL + '?tab=repositories'

        html_content = requests.get(reposURL).text
        soup = BeautifulSoup(html_content, 'html.parser')
        star_count = soup.find_all('a', attrs={'class': 'Link--muted mr-3'})
        repo_name = soup.find_all('p', attrs={'class': 'col-9 d-inline-block color-fg-muted mb-2 pr-4'})

        i = [] # star count
        j = [] #repo names
        final = {} #final list

        for tag in star_count:
            i.append(tag.text.strip())

        for tag in repo_name:
            j.append(tag.text.strip())

        final = {key:value for key, value in zip(j, i)} #final list

        return final
    except:
        final = {repo_name:"",star_count:""}
        return final
