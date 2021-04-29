import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://play.google.com/store/search?q=food%20de&c=apps")
time.sleep(10)
SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
time.sleep(SCROLL_PAUSE_TIME)

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

links_games = []
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    if "details?id" in elem.get_attribute("href"):
        links_games.append((elem.get_attribute("href")))

links_games = list(dict.fromkeys(links_games))
#print(links_games)
list_all_elements = []
for iteration in links_games:
    try:
        driver.get(iteration)
        print(iteration)
        time.sleep(3)

        header1 = driver.find_element_by_tag_name("h1")
        star = driver.find_element_by_class_name("BHMmbe")

        others = driver.find_elements_by_class_name("htlgb")
        list_others = []
        for x in range(len(others)):
            if x % 2 == 0:
                list_others.append(others[x].text)

        titles = driver.find_elements_by_class_name("BgcNfc")
        comments = driver.find_element_by_class_name("EymY4b")

        list_elements = [iteration, header1.text, float(star.text.replace(",", ".")), comments.text.split()[0]]
        for x in range(len(titles)):
            if titles[x].text == "Installs":
                list_elements.append(list_others[x])
            if titles[x].text == "Developer":
                for y in list_others[x].split("\n"):
                    if "@" in y:
                        list_elements.append(y)
                        break

        list_all_elements.append(list_elements)

    except Exception as e:
        print(e)
df = pd.DataFrame(list_all_elements,columns = ['URL', 'Name', 'Stars', 'Total_Reviews'])
df.to_csv('Food_Apps.csv',index = False,header = True,encoding = 'utf-8')




'''
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd

my_url = "https://play.google.com/store/search?q=food%20delivery%20apps&c=apps"

uCLient = uReq(my_url)
page_html = uCLient.read()
uCLient.close()
page_soup = bs(page_html,"html.parser")

containers = page_soup.findAll("div",{"class":"ImZGtf mpg5gc"})
#print(len(containers))

#print(bs.prettify((containers[0])))

container = containers[1]
Title = container.find("div",{"class":"WsMG1c nnK0zc"})['title'].split()[0]
#print(Title)
Rating = container.find("div",{"class":"pf5lIe"}).div.get('aria-label')
Rating = container.find("div",{"class":"pf5lIe"}).div['aria-label'].split()[1]
#print(Rating)

List = []

for container in containers:
    App_Name = container.find("div",{"class":"WsMG1c nnK0zc"})['title'].split()[0]
    Stars = container.find("div",{"class":"pf5lIe"}).div['aria-label'].split()[1]
    List.append([App_Name,Stars])
    df = pd.DataFrame(List,columns = ['App Name','Rating'])

df.to_csv('Food_Apps_Info.csv',index = False,encoding = 'utf-8')
'''