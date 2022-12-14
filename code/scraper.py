# webscraper
#------------------------------------------------------------------------------
from os import remove
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import datetime


# preparation
#------------------------------------------------------------------------------


class Article:
    def __init__(self) -> None:    
        self.paper = ""
        self.title = ""
        self.link = ""
        self.author = []
        self.date = None
        self.premium = None
        self.length = 0
        self.articleType = 0
        self.position = None
        self.wordlength = 0

todaysdate = datetime.datetime.now().strftime("%Y-%m-%d")

# FAZ
#------------------------------------------------------------------------------

fazArticles = []

# variables specific to FAZ
URL = "https://www.faz.net/aktuell/"
divArticle = "tsr-Base_ContentWrapperInner teaserInner linkable"
headlineElement = "span"
headlineName = "tsr-Base_HeadlineText"
articleLinkName = "js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink"
textClassName="atc-TextParagraph"

#download the main page
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# with open('datadump/output.html', 'w') as f:
#         f.write(soup.prettify())


# find all articles
article_divs = soup.find_all("div", class_=divArticle)


for k, article_div in enumerate(article_divs):
    fazArticles.append(Article())
    fazArticles[-1].paper = "FAZ"
    fazArticles[-1].title = article_div.find(headlineElement, class_ = headlineName).text.strip() #find html element span with class :...
    fazArticles[-1].link = article_div.find("a", class_=articleLinkName)["href"]
    if article_div.find("a", class_=articleLinkName)["data-is-premium"] == "true":
        fazArticles[-1].premium = 1
    else:
        fazArticles[-1].premium = 0
    fazArticles[-1].date = todaysdate
    fazArticles[-1].position = k


for article in list(fazArticles): #list because remove wont work otherwise
    page = requests.get(article.link)
    soup = BeautifulSoup(page.content, "html.parser")

    #author
    authorLink = soup.find_all("span","atc-MetaAuthorText")
    if len(authorLink) > 0:
        for al in authorLink:
            authorname = al.findNext("span").text
            article.author.append(al.findNext("span").text)

    #length
    textparagraghs = soup.findAll("p", class_ = textClassName)
    length = 0
    for par in textparagraghs:
        length += len(par.text.split())
    article.length = length
    
    if len(article.author) == 0 :
        fazArticles.remove(article)

    if article.length == 0:
        fazArticles.remove(article)


# Zeit
#------------------------------------------------------------------------------

zeitArticles = []

URL = "https://www.zeit.de/index"
divArticle = "zon-teaser-standard__container" #"zon-teaser-standard__combined-link" 
headlineElement = "span"
headlineName = "zon-teaser-standard__title"
articleLinkName = "zon-teaser-standard__heading-link"
zplus = "zplus-badge zplus-badge--coverless" #div in article for premium
authorLink = "https://www.zeit.de/autoren/R"
textClassName = "paragraph article__item"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

article_divs = soup.find_all("article")

print(len(article_divs))

for k, article_div in enumerate(article_divs):
    zeitArticles.append(Article())
    zeitArticles[-1].paper = "Zeit"
    zeitArticles[-1].title = article_div.find("a").text.strip()
    zeitArticles[-1].link = article_div.find("a")["href"]
    zeitArticles[-1].date = todaysdate
    zeitArticles[-1].position = k

for article in list(zeitArticles):
    page = requests.get(article.link)
    soup = BeautifulSoup(page.content, "html.parser")

    #author
    if soup.find("a",rel="author") != None:
        article.author = soup.find("a",rel="author").find("span").text
    elif soup.find("span",class_="metadata__source") != None and soup.find("span",class_="metadata__source").find("a") != None:
        article.author = soup.find("span",class_="metadata__source").find("a")["href"].split("/")[3]

    #premium
    if soup.find("span", class_ = "zplus-badge__link-text") != None:
        article.premium = 1
    else:
        article.premium = 0
    
    #length
    textparagraghs = soup.findAll("p",class_ = textClassName)
    length = 0
    for par in textparagraghs:
        length += len(par.text.split())
    article.length = length

    #filter
    if article.length == 0:
        zeitArticles.remove(article)
    elif len(article.author) == 0:
        zeitArticles.remove(article)
    elif article.link.find("https://www.zeit.de") == None:
        zeitArticles.remove(article)


#database
#------------------------------------------------------------------------------

def insertArticle(article, dbcon):
    #print(f''' INSERT INTO ZEITUNG (ZEITUNGSNAME,RELEASEDATE,PREMIUM,LENGTH,TITLE,TYPE,WORDLENGTH,POSITION, AUTHOR, LINK) VALUES
    #                ('{article.paper}', '{article.date}', {article.premium}, {article.length}, '{article.title.replace("'", "`")}', '{article.articleType}', {article.wordlength}, {article.position}, '{json.dumps(article.author)}', '{article.link}') ''')
    dbcon.execute(f''' INSERT INTO ZEITUNG (ZEITUNGSNAME,RELEASEDATE,PREMIUM,LENGTH,TITLE,TYPE,WORDLENGTH,POSITION, AUTHOR, LINK) VALUES
                    ('{article.paper}', '{article.date}', {article.premium}, {article.length}, '{article.title.replace("'", "`")}', '{article.articleType}', {article.wordlength}, {article.position}, '{json.dumps(article.author)}', '{article.link}') ''')


with sqlite3.connect("database/data.db") as dbcon:
    print("database connect")

    a =  dbcon.execute('''SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ZEITUNG';''')
    if a.fetchone()[0] != 1:
        dbcon.execute('''CREATE TABLE ZEITUNG
        (ID              INTEGER         NOT NULL PRIMARY KEY AUTOINCREMENT,
        ZEITUNGSNAME     VARCHAR         NOT NULL,
        AUTHOR           JSON            NOT NULL,
        RELEASEDATE      DATE            NOT NULL,
        PREMIUM          BOOL            ,
        LENGTH           INT             NOT NULL,
        TITLE            VARCHAR         NOT NULL,
        TYPE             VARCHAR         ,
        WORDLENGTH       DECIMAL         ,
        POSITION         INT             ,
        LINK             VARCHAR         NOT NULL);''')

    for art in fazArticles:
        insertArticle(art,dbcon)
    for art in zeitArticles:
        insertArticle(art,dbcon)

    dbcon.commit()

#webscraper tutorial
# tutorial at https://realpython.com/beautiful-soup-web-scraper-python/
#------------------------------------------------------------------------------

'''
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL) #can also du post with payload, more in ecampusscraper
                        # inspect firefox for payload -> network i believe


with open('datadump/output.html', 'w') as f:
        f.write(page.text)

soup = BeautifulSoup(page.content, "html.parser") #page.content is bite representation -> character errors... 

# dyamic sites: requests-html, Selenium


results = soup.find(id="ResultsContainer") # id is unique

print(results.prettify())

job_elements = results.find_all("div", class_="card-content")


# get html things from each container
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()

python_jobs = results.find_all("h2", string="Python") #looks for Python in any h2 element 


python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower() #converts strings to lowercase before comparison i.e. text is html element text
)

print(python_jobs[0])

python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs #get grand parent element from h2 lements
]

for job_element in python_job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
    links = job_element.find_all("a") # get all <a> tags
    for link in links:
        link_url = link["href"] # get the href attribute
        print(f"Apply here: {link_url}\n")
        
'''