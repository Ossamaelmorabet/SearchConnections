import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter


testExcel = xlsxwriter.Workbook("liste_des_connections.xlsx")
worksheet = testExcel.add_worksheet("mes connections sur Linkedin")

##warnings.filterwarnings("ignore", category=UserWarning)



#login to linkedin
os.environ['PATH'] += r"C:\SeleniumDrivers"
ourDriver = webdriver.Chrome()
ourDriver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
username = ourDriver.find_element(By.ID, "username")
password = ourDriver.find_element(By.ID, "password")
print("saisir votre email")
username.send_keys(input())
print("saisir votre mot de passe")
password.send_keys(input())

try:
    button = WebDriverWait(ourDriver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space(@aria-label = 'Sign/ in')]"))
    )
    button.click()
except Exception as e:
    print(e)
    print("button error")

#click to my profile
try:
    profileLink = WebDriverWait(ourDriver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Ossama El Morabet"))
    )
    profileLink.click()
except Exception as e:
    print(e)
    print("profile error")

#check my connections
try:
    connections = WebDriverWait(ourDriver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='link-without-visited-state']"))
    )
    connections.click()
except Exception as e:
    print(e)

    print("profile error")


def getProfiles(source_page , driver ):
        tabs = source_page.findAll('li', class_='reusable-search__result-container')
        data = []
        for tab in tabs:
            profile_connection = tab.find('a', class_='app-aware-link')
            driver.get(profile_connection.get('href'))
            connection_info = BeautifulSoup(driver.page_source, 'html.parser')
            headline = connection_info.find('div', class_='text-body-medium break-words')
            about = connection_info.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed')
            openToWork = connection_info.find('div', class_='pv-open-to-carousel')
            sleep(2)
            if openToWork:
                print(1)
                profilelink= profile_connection.get('href')
                print((profilelink.split('?'))[0])
                data.append((profilelink.split('?'))[0])
            elif about:
                print(2)
                if "Java" in headline.text or "Java" in about.text:
                    profilelink = profile_connection.get('href')
                    data.append((profilelink.split('?'))[0])
            else:
                print(3)
                if "Java" in headline.text:
                    profilelink = profile_connection.get('href')
                    data.append((profilelink.split('?'))[0])

            sleep(2)
            ourDriver.back()

        return data

for page in range(30):
    try:
        sleep(2)
        urls = getProfiles(BeautifulSoup(ourDriver.page_source, 'html.parser'), ourDriver)
       ## print(urls)
        x=1
        for url in urls:
                worksheet.write(x, 0, url)
                x=x+1
        sleep(2)
        ourDriver.execute_script('window.scrollTo(0 , document.body.scrollHeight);')
        nextBtn = WebDriverWait(ourDriver, 5000).until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Next']"))
        )
        nextBtn.click()
    except Exception as e:
        print(e)
        print("next error")

testExcel.close()

# def ocrOpenToWork(path):
#     try:
#         reader = easyocr.Reader(['en'], gpu=False , verbose=False)
#         result = reader.readtext(path)
#         sleep(2)
#         res = [ele for sub in result for ele in sub if isinstance(ele, str)][0]
#     except:
#         print("error Image")
#     return res

