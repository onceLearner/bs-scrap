from requests import get
from bs4 import BeautifulSoup
import json
import re


url = "https://www.emploi.ma/recherche-jobs-maroc?page=0"
url_page2= "https://www.emploi.ma/recherche-jobs-maroc?page=1"
# getting the html  document  from the page
response = get(url_page2);

# load the page into beautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

array_all_jobs = []


all_jobs_divs=soup.find_all("div","job-title")

for item in all_jobs_divs :
    array_all_jobs.append(item.findNext().findNext()['href'])




