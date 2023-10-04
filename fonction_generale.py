# import
import feedparser
import flux_rss
import page_liens
import historique
import pprint
from bs4 import BeautifulSoup
import requests

# init
nouvelles_actus = {}
historique_memoire = []


def lecture_fichier_rss(salons):
    
    
    # init
    global nouvelles_actus
    nouvelles_actus = {}
    
    
    # FR: Parcours des sites et de leurs liens RSS dans le fichier flux_rss
    # EN: Loop through the sites and their RSS links in the flux_rss file
    for site in flux_rss.flux_rss:
        for nom_site, liens_rss in site.items():
            for lien, categorie in liens_rss.items():

                rss_url = lien
                # FR: Charger le fichier XML RSS
                # EN: Load the RSS XML file
                feed = feedparser.parse(rss_url)
                print(lien)

                # FR: Accéder aux éléments du flux RSS
                # EN: Access the elements of the RSS feed
                for entry in feed.entries:
                    lien_actu = entry.link
                    
                    # FR: Vérifier si le lien n'est pas déjà dans l'historique
                    # EN: Check if the link is not already in the history
                    if lien_actu not in historique.historique and lien_actu not in historique_memoire:
                        id_cated = salons[categorie]
                        id_site = salons[nom_site]
                        
                        # FR: Stocker le lien et ses catégories correspondantes
                        # EN: Store the link and its corresponding categories
                        nouvelles_actus[lien_actu] = [id_site,id_cated]
                        historique.historique.append(lien_actu)
                        historique_memoire.append(lien_actu)
    pprint.pprint(nouvelles_actus)


def lecture_fichieru_url(salons):
    global nouvelles_actus
    news = []
    nouvelles_actus = {}
    
    # FR: Parcours des sites et de leurs liens dans le fichier page_liens
    # EN: Loop through the sites and their links in the page_liens file
    for site in page_liens.sites:
        for nom_site, liens in site.items():
            print(nom_site)
            lien_site_original = list(liens.keys())[-1]
            for lien, categorie in liens.items():
                print(lien+" - "+categorie)
                
                # FR: Vérifier la connexion au site
                # EN: Check the connection to the website
                if connexion_site(lien):
                    news = extrait_balise_a_et_recherche_nouveau_lien(lien_site_original, lien)
                    rangement_lien(news, nom_site, salons)
    pprint.pprint(nouvelles_actus)



def connexion_site(url):
        
    # FR: Fonction pour établir une connexion à un site web donné
    # EN: Function to establish a connection to a given website
    global reponse
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            connexion = True

        else:
            print(url + ": La connexion au site web a échoué. Code de statut :", reponse.status_code)
            connexion = False

    
    except requests.exceptions.RequestException as e:

        print("Une erreur s'est produite lors de la connexion :", str(e))
        connexion = False
    
    return connexion


def extrait_balise_a_et_recherche_nouveau_lien(pre_lien, url):
    
    # init
    nouveau_lien = []
    href_sans_htpp = ""
    global reponse
    contenue_page = reponse.text
    soup = BeautifulSoup(contenue_page, 'html.parser')
    
    # FR: Récupérer la valeur de l'attribut href dans les balises <a>
    # EN: Get the value of the href attribute in <a> tags
    tout_les_liens_a = soup.find_all('a')

    for lien in tout_les_liens_a:
        try:
            href = lien.get('href')

            if "#" in href:
                href = href.split("#")[0]
            
            if not "https:/" in href and not "http:/" in href:
                href_sans_htpp = href
                href = pre_lien + href
                
            href = href.replace("//", "/")
            href = href.replace("https:/", "https://")
            href = href.replace("http:/", "http://")
            href_sans_htpp = href.replace("https://", "http://")
            href_sans_pre_lien = href.replace(url, "")

            
            # FR: Vérifier si le lien n'est pas déjà dans l'historique
            # EN: Check if the link is not already in the history
            if href in historique.historique or href_sans_htpp in historique.historique or href_sans_pre_lien in historique.historique or href in historique_memoire or href_sans_htpp in historique_memoire or href_sans_pre_lien in historique_memoire :
                continue
            
            else:
                historique.historique.append(href)
                historique.historique.append(href_sans_pre_lien)
                historique.historique.append(href_sans_htpp)
                historique_memoire.append(href)
                historique_memoire.append(href_sans_pre_lien)
                historique_memoire.append(href_sans_htpp)
                nouveau_lien.append(href)
               
        except:
            continue

    return nouveau_lien


# FR: Fonction qui organise les liens en fonction de leur site d'origine et de leur catégorie
# EN: Function that organizes links based on their original site and category
def rangement_lien(nouvelle_news, nom_site, salons):

    # init
    global nouvelles_actus

    for lien in nouvelle_news:
        liens_trouve = ""
        categ_trouve = ""
        for site in page_liens.sites:
                for nom_site_lien, liens in site.items():
                    if nom_site_lien == nom_site:
                        for lien_lie, categ in liens.items():

                            # FR: Vérifie si le nom du lien est contenu dans le lien actuel et s'il est plus long que ce qui a été trouvé précédemment
                            # EN: Checks if the link name is contained in the current link and if it's longer than what was found previously
                            if lien_lie in lien and len(liens_trouve) < len(lien_lie):
                                liens_trouve = lien_lie
                                categ_trouve = categ
        
        if liens_trouve != "":
            id_cated = salons[categ_trouve]
        else:
            id_cated = salons["autres"]

        id_site = salons[nom_site]
        nouvelles_actus[lien] = [id_site,id_cated]
