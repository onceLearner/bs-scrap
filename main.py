from bsMethods import scrap_emploi

#test urls
url = "https://www.emploi.ma/offre-emploi-maroc/charge-projets-etudes-developpement-si-5505498"
url2 = "https://www.emploi.ma/offre-emploi-maroc/teleprospectrices-urgent-marrakech-6058749"
url3 = "https://www.emploi.ma/offre-emploi-maroc/directeur-production-agroalimentaire-nouakchott-mauritanie-6141015"
url4_multiplelang= "https://www.emploi.ma/offre-emploi-maroc/anglais-espagnol-tour-operator-reception-appel-6220371"


user_url =  str(input("tapper un lien d'une page d'annonce sur emploi.ma \n"))

scrap_emploi(user_url)
