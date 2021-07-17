from requests import get
from bs4 import BeautifulSoup
import json
import re
import datetime


def convert_date_to_numbers(str_date):
    date = datetime.date
    if(str_date.split(" ")[0]=="aujourd'hui") :
        return date.today()
    offset = str_date.split("il y a ")[1].split(" ")[0]
    return date.today()- datetime.timedelta(days=int(offset))



# convert_date_to_numbers("il y a 3 jours sur ReKrute.com - Postuler avant le 14/09/2021")

def remove_more_than_one_space(str):
    return ' '.join(str.split())

def scrap_announces_url_into_array_from_Rekrute(number_of_pages):

    # array to be returned
    array_all_jobs = []

    # url to the page
    url = "https://www.rekrute.com/offres.html?s=2&"

    # iterate depending on the number of pages we want to scrap
    for i in range(number_of_pages):
      #load the page into beautifulSoup
      response = get( url+"p={}".format(i));
      soup = BeautifulSoup(response.text, 'html.parser')
      all_jobs_divs = soup.find_all("li", "post-id")

      for item in all_jobs_divs:
          array_all_jobs.append(item.findNext().findChildren("div", recursive=False)[1].findNext().findNext().findNext()['href'])


    for item in array_all_jobs:
        print(item)

    #return  array_all_jobs




def scrap_page_rekrute(url):
    # getting the html  document  from the page
    response = get(url);

    # load the page into beautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    #data we want to scrap
    scrapped_data = dict(
        title='a',
        number_posts=1,
        publication_date=dict(
            day=1,
            month=1,
            year=2020
        ),
        company=dict(
            title='a',
            sector=[
            ],
            website=None,
            description='ab'
        ),
        metiers=[
            'a', 'b'
        ],
        sector_activity=[
            'a', 'b'
        ],
        profile=[
            'a', 'b'
        ],
        skills=[

        ],
        contract_type='',
        region='', city='',
        level_experience='',
        level_studies='',
        languages=dict(

        ))

    scrapped_data['title']=soup.find("h1").text

    main_info = soup.find('ul','featureInfo').findChildren('li')
    scrapped_data['level_experience'] =main_info[0].text.strip()

    #' '.joint(str.split()) is to remore more than 1  space
    scrapped_data['level_studies']=' '.join(main_info[2].text.strip().replace("\n","").replace("\r","").replace("\t","").split())
    scrapped_data['number_posts']=main_info[1].text.split(" ")[0].strip()
    scrapped_data['city'] =str(main_info[1].text.split("sur")[1]).strip().split("et")[0]
    scrapped_data['region']=str(main_info[1].text.split("sur")[1]).strip().split("et")[0]

    scrapped_data['contract_type']= soup.find('span','tagContrat').text.strip()

    scrapped_data['company']['title'] = soup.find("head").text.split("-")[2].strip()
    scrapped_data['company']['description'] = soup.find('div',id='recruiterDescription').text.split("Entreprise :")[1].strip()


    scrapped_data['metiers'] = ' '.join(soup.find('h2').text.strip().replace("\n","").replace("\r","").split()).split("- Secteur")[0].split("/")
    scrapped_data['sector_activity'] = ' '.join(soup.find('h2').text.strip().replace("\n","").replace("\r","").split()).split("- Secteur")[1].split("/")

    scrapped_data['skills'] = [ item.text.strip() for item in soup.find_all('span',"tagSkills") ]
    scrapped_data['profile'] = soup.find(text=re.compile('Profil recherché')).parent.parent.text.strip().split("Profil recherché :")[1].replace("\t","").split("\n")

    publication_date = convert_date_to_numbers(remove_more_than_one_space(soup.find("span","newjob").text).split("Publiée ")[1])

    scrapped_data['publication_date']['day']=publication_date.day
    scrapped_data['publication_date']['month']=publication_date.month
    scrapped_data['publication_date']['year']=publication_date.year


    found = soup.find(text=re.compile('Profil recherché')).parent.parent.text.strip().split("Profil recherché :")[1].replace("\t","").split("\n")
    #print([ item.text.strip() for item in found ])
    serialized = json.dumps(scrapped_data, indent=4, ensure_ascii=False);
    print(serialized)
    print(remove_more_than_one_space(soup.find("span","newjob").text).split("Publiée "))
    return serialized
    return "hh"



url = "https://www.rekrute.com/offre-emploi-responsable-fusion-four-a-arc-electrique-recrutement-meski-invest---riva-industries-el-jadida-126810.html"

url2 = "https://www.rekrute.com/offre-emploi-gestionnaires-portefeuilles-clients-recrutement-manpower-agences-tanger-126808.html"

url3 = "https://www.rekrute.com/offre-emploi-stagiaire-technicien-helpdesk-hf-recrutement-umanis-casablanca-126802.html"

url4_old = "https://www.rekrute.com/offre-emploi-ingenieur-etude-et-developpement-.net-senior-hf-recrutement-neosys-casablanca-126725.html"

scrap_page(url4_old)
