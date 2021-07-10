from requests import get
from bs4 import BeautifulSoup
import json
import re

url = "https://www.emploi.ma/offre-emploi-maroc/charge-projets-etudes-developpement-si-5505498"
url2 = "https://www.emploi.ma/offre-emploi-maroc/teleprospectrices-urgent-marrakech-6058749"
url3 = "https://www.emploi.ma/offre-emploi-maroc/directeur-production-agroalimentaire-nouakchott-mauritanie-6141015"
url4_multiplelang = "https://www.emploi.ma/offre-emploi-maroc/anglais-espagnol-tour-operator-reception-appel-6220371"


def scrap_announces_url_into_array(number_of_pages):

    # array to be returned
    array_all_jobs = []

    # iterate depending on the number of pages we want to scrap
    for i in range(number_of_pages):
      #load the page into beautifulSoup
      response = get("https://www.emploi.ma/recherche-jobs-maroc?page={}".format(i));
      soup = BeautifulSoup(response.text, 'html.parser')
      all_jobs_divs = soup.find_all("div", "job-title")

      for item in all_jobs_divs:
          array_all_jobs.append(item.findNext().findNext()['href'])


    return  array_all_jobs






def scrap_emploi(url):
    # getting the html  document  from the page
    response = get(url);

    # load the page into beautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # the data we want to scrap
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
                'a',
                'b'
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
        contract_type='',
        region='', city='',
        level_experience='',
        level_studies='',
        languages=dict(

        ))

    # Now let's start filling the dictionary
    scrapped_data['title'] = soup.find("h1", "title").text
    scrapped_data['number_posts'] = soup.find("td", text="Nombre de poste(s) : ").findNext().text

    date_array = soup.find("div", "job-ad-publication-date").text.split(" ")[2].split(".")
    scrapped_data['publication_date']['day'] = date_array[0]
    scrapped_data['publication_date']['month'] = date_array[1]
    scrapped_data['publication_date']['year'] = date_array[2]

    scrapped_data['company']['title'] = soup.find("div", "company-title").text
    scrapped_data['company']['sector'] = soup.find("div", "field-name-field-entreprise-secteur").text.split(",") if soup.find("td",
                                                                                                   "field-name-field-entreprise-secteur") else None
    scrapped_data['company']['website'] = soup.find("td", "website-url").text.strip() if soup.find("td",
                                                                                                   "website-url") else None
    scrapped_data['company']['description'] = \
        soup.find("div", "job-ad-company-description").text.split("Description de l'entreprise")[1].strip()

    scrapped_data['sector_activity'] = soup.find("div", "field-name-field-offre-secteur").text.split()
    scrapped_data['metiers'] = soup.find("div", "field-name-field-offre-metiers").text.split()

    scrapped_data['profile'] = soup.find(text=re.compile('Profil')).findNext().text.strip().split("\n")
    scrapped_data['contract_type'] = soup.find('div', "field-name-field-offre-contrat-type").text
    scrapped_data['region'] = soup.find('div', "field-name-field-offre-region").text
    scrapped_data['city'] = soup.find('td', text=re.compile("Ville : ")).findNext().text if soup.find('td', text=re.compile("Ville : ")) else None
    scrapped_data['level_experience'] = soup.find('div', "field-name-field-offre-niveau-experience").text
    scrapped_data['level_studies'] = soup.find('div', "field-name-field-offre-niveau-etude").text

    if soup.find('div', "field-name-field-offre-niveau-langue"):
     for elt in soup.find('div', "field-name-field-offre-niveau-langue").findNext().findChildren("div", recursive=False):
        scrapped_data['languages'][elt.text.split('›')[0]] = elt.text.split('›')[1]

    # create json object,
    serialized = json.dumps(scrapped_data, indent=4,ensure_ascii=False);
    return serialized
