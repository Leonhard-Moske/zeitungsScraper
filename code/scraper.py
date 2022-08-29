# webscraper
#------------------------------------------------------------------------------
from types import NoneType
import requests
from bs4 import BeautifulSoup

# FAZ
#------------------------------------------------------------------------------


URL = "https://www.faz.net/aktuell/"
divArticle = "tsr-Base_ContentWrapperInner teaserInner linkable"
headlineElement = "span"
headlineName = "tsr-Base_HeadlineText"
articleLinkName = "js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink"

page = requests.get(URL)
#with open('datadump/output.html', 'w') as f:
#        f.write(page.text)

soup = BeautifulSoup(page.content, "html.parser")

with open('datadump/output.html', 'w') as f:
        f.write(soup.prettify())

article_divs = soup.find_all("div", class_=divArticle)

#print(len(article_divs))

for article_div in article_divs:
    print(article_div.find(headlineElement, class_ = headlineName).text.strip()) #find html element span with class :...
    print("\t",article_div.find("a", class_=articleLinkName)["href"])    

#print(len(article_divs))


# Zeit
#------------------------------------------------------------------------------

URL = "https://www.zeit.de/index"
divArticle = "zon-teaser-standard__container" #"zon-teaser-standard__combined-link" 
headlineElement = "span"
headlineName = "zon-teaser-standard__title"
articleLinkName = "zon-teaser-standard__heading-link"

page = requests.get(URL)
#with open('datadump/output.html', 'w') as f:
#        f.write(page.text)

soup = BeautifulSoup(page.content, "html.parser")

with open('datadump/output.html', 'w') as f:
        f.write(soup.prettify())

article_divs = soup.find_all("div", class_=divArticle)

print(len(article_divs))

for article_div in article_divs:
    #print(article_div)
    #print(article_div.find(headlineElement, class_ = headlineName).text.strip()) #find html element span with class :...
    a = article_div.find("a", class_=articleLinkName)
    if type(a) != NoneType:
        print("\t",article_div.find("a", class_=articleLinkName)["href"])
    else:
        print("sonder")
        print("\t",article_div.parent["href"])

print(len(article_divs))

#database
#------------------------------------------------------------------------------


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