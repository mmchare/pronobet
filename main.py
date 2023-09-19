# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import json
import asyncio
from twilio.rest import Client
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import os
from dotenv import load_dotenv

load_dotenv()

async def pronobet():
    cookies = json.loads(open("bing_cookies_123.json", encoding="utf-8").read())


    #Définir l'URL du site à scraper
    url = os.getenv("URL")
    url2 = os.getenv("URL2")

    # Envoyer une requête HTTP GET pour récupérer le contenu de la page
    response = requests.get(url)
    response_2 = requests.get(url2)

    # Vérifier le statut de la réponse (200 signifie succès)
    if response.status_code == 200 & response_2.status_code == 200:
        # Créer un objet BeautifulSoup à partir du contenu HTML de la réponse
        soup = BeautifulSoup(response.content, "html.parser")
        soup2 = BeautifulSoup(response_2.content, "html.parser")

        # Trouver le premier élément <script> qui a l'id "__NEXT_DATA__"
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        script2 = soup2.find("script", {"id": "__NEXT_DATA__"})

        # Extraire le contenu de l'élément sous forme de chaîne de caractères
        data = script.string
        data2 = script2.string

        # Convertir la chaîne de caractères en un objet Python
        data = json.loads(data)
        data2 = json.loads(data2)

        # On accède à la liste des objets qui se trouve dans le dictionnaire
        liste = data2['props']['pageProps']['data'][0]['data']

        # On définit une fonction qui renvoie la valeur de l'élément "time" d'un objet
        def get_time(objet):
            return objet['time']

        # On trie la liste des objets selon la valeur de l'élément "time" par ordre croissant
        # On utilise la fonction get_time comme clé de tri
        liste.sort(key=get_time)

        # On utilise la notation par tranches pour extraire les 4 premiers éléments de la liste
        # Le premier indice est 0 et le dernier indice est exclu, donc on utilise [0:4]
        quatre_premiers_objets = liste[0:4]

        # On affiche les 4 premiers objets
        ##########print(quatre_premiers_objets)

        def get_profit_2(objet):
            return objet['profit']

        # On trie la liste des objets selon la valeur de l'élément "profit" par ordre décroissant
        # On utilise la fonction get_profit comme clé de tri
        # On ajoute le paramètre reverse=True pour inverser l'ordre du tri
        liste.sort(key=get_profit_2, reverse=True)

        # On utilise la notation par tranches pour extraire les 4 premiers éléments de la liste
        # Le premier indice est 0 et le dernier indice est exclu, donc on utilise [0:4]
        quatre_premiers_objets_2 = liste[0:4]

        # On affiche les 4 premiers objets
        #########print(quatre_premiers_objets_2)



        

        # Afficher l'objet Python
        #print(data2)

        # Créer une liste vide pour stocker les objets filtrés
        filtered_list = []

        # Parcourir la liste des objets dans le dictionnaire
        for obj in data['props']['pageProps']['data']:
            sport_id = obj['sport_id']
            league = obj['league']
            home = obj['home']
            away = obj['away']
            odds_moneyline = obj['odds_moneyline']

            # Calculer les pourcentages à partir des cotes odds-moneyline
            # Formule : pourcentage = 1 / (cote) * 100
            # home_percentage = 1 / (odds_moneyline['home'] + 1) * 100
            # away_percentage = 1 / (odds_moneyline['away'] + 1) * 100

            if sport_id == '1' :
                home_percentage = 1 / (odds_moneyline['home']) * 100
                away_percentage = 1 / (odds_moneyline['away']) * 100
                draw_percentage = 1 / (odds_moneyline['draw']) * 100

                if home_percentage > away_percentage + draw_percentage :
                    id_1 = {"type" : sport_id,"league" : league, "home" : home,"away" : away, "home_percentage" : home_percentage, "away_percentage": away_percentage, "max": home_percentage}
                    filtered_list.append(id_1)
                elif away_percentage > home_percentage + draw_percentage :
                    id_2 = {"type" : sport_id,"league": league, "home": home, "away": away, "home_percentage": home_percentage,
                        "away_percentage": away_percentage, "max": away_percentage}
                    filtered_list.append(id_2)

            elif sport_id == '2' :
                home_percentage = 1 / (odds_moneyline['home']) * 100
                away_percentage = 1 / (odds_moneyline['away']) * 100

                if home_percentage > away_percentage * 1.5 :

                    id_1 = {"type" : sport_id,"league": league, "home": home, "away": away, "home_percentage": home_percentage,
                        "away_percentage": away_percentage, "max": home_percentage}
                    filtered_list.append(id_1)
                elif away_percentage > home_percentage * 1.5 :
                    id_2 = {"type" : sport_id,"league": league, "home": home, "away": away, "home_percentage": home_percentage,
                        "away_percentage": away_percentage, "max": away_percentage}
                    filtered_list.append(id_2)

            elif sport_id == "3" :
                home_percentage = 1 / (odds_moneyline['home']) * 100
                away_percentage = 1 / (odds_moneyline['away']) * 100

                if home_percentage > away_percentage * 2:

                    id_1 = {"type" : sport_id,"league": league, "home": home, "away": away, "home_percentage": home_percentage,
                        "away_percentage": away_percentage, "max": home_percentage}
                    filtered_list.append(id_1)
                elif away_percentage > home_percentage * 2:

                    id_2 = {"type" : sport_id,"league": league, "home": home, "away": away, "home_percentage": home_percentage,
                        "away_percentage": away_percentage, "max": away_percentage}
                    filtered_list.append(id_2)

            else : print("Erreur pas de compatibilité")

        # Créer un dictionnaire vide pour stocker le plus grand max par type 653612822
        max_par_type = {}


        # Parcourir le tableau d'objets
        for objet in filtered_list:
            # Extraire le type et le max de l'objet
            type = objet["type"]
            max = objet["max"]
            # Vérifier si le type existe déjà dans le dictionnaire
            if type in max_par_type:
                # Comparer le max de l'objet avec les deux plus grands max du type
                if max > max_par_type[type][0]:
                    # Mettre à jour les deux plus grands max du type avec le max de l'objet et l'ancien plus grand max
                    max_par_type[type] = [max, max_par_type[type][0]]
                elif max > max_par_type[type][1]:
                    # Mettre à jour le deuxième plus grand max du type avec le max de l'objet
                    max_par_type[type][1] = max
            else:
                # Ajouter le type et le max de l'objet au dictionnaire comme une liste de deux éléments
                max_par_type[type] = [max, -float("inf")]

        # Créer une liste vide pour stocker les éléments retenus
        elements_retenus = []

        # Parcourir à nouveau le tableau d'objets
        for objet in filtered_list:
            # Extraire le type et le max de l'objet
            type = objet["type"]
            max = objet["max"]
            # Vérifier si le max de l'objet correspond à l'un des deux plus grands max du type
            if max in max_par_type[type]:

                _objet = f"League {league}. équipes {home} vs {away}, {home} a {home_percentage:.2f}% de chances de gagner,"

                # Ajouter l'objet à la liste des éléments retenus
                elements_retenus.append(objet)

        # Afficher la liste des éléments retenus
        print(elements_retenus)

        _prompt = f"voici un tableau fournissant des informations sur differents types de paris sportif: {elements_retenus} .J'aimerais que tu analyses ce tableau et que tu me fournis des resultat claire, nette, concis pour chaque objet. Par exemple pour l'objet 1 tu dois dire: type: Football, league: Norwayn Toppserien women, équipe: Rosenborg BK Kvinner vs Arna-Bjornar et Rosenborg BK Kvinner gagne. remarque que l'equipe ou le joueur qui gagne est en fonction de la probabilité de gain 'away_percentage' ou 'home_percentage'.mais il est important que tu sois très court et concis et que tu ne choisi que les match d'aujourd'hui donc ne fournis que des informations extremement nécessaires, evite s'il te plait de te presenter au debut et d'ajouter des informations qui ne servent à rien. et pour chaque confrontation donne la date et l'heure pour un habitant du cameroun ajoute aussi la cote du favorie selon 1xbet cameroun et plus important encore la longueur de ta reponse ne dois pas depasser 1600 caracteres c'est tres important soit extrement court"

        ##chareGPT(elements_retenus)
        # Passing cookies is "optional", as explained above
        bot = await Chatbot.create(cookies=cookies)

        response = await bot.ask(prompt=_prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
        print(response['text'])
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        # Use a breakpoint in the code line below to debug your script.
        # les credentials sont lues depuis les variables d'environnement TWILIO_ACCOUNT_SID et AUTH_TOKEN
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # c'est le numéro de test de la sandbox WhatsApp
        from_whatsapp_number = os.getenv("FROM_WHATSAPP_NUMBER")
        # remplacez ce numéro avec votre propre numéro WhatsApp not-carry  not-carry
        to_whatsapp_number = os.getenv("TO_WHATSAPP_NUMBER")
        message = client.messages.create(body=response['text'],
                                         from_=from_whatsapp_number,
                                         to=to_whatsapp_number)

        ##Afficher la liste filtrée
        #print(filtered_list)
    else:
        # Afficher un message d'erreur
        print("Le web scraping a échoué ! Le statut de la réponse est :", response.status_code)















# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(pronobet())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/














'''

voici un tableau contennant des fournissant des informations sur differents types de paris sportif:{}
 J'aimerais que tu analyses ce tableau et que tu me fournis des resultat claire et nette pour chaque objet. 
 Par exemple pour l'objet 1 tu peux dire: type: Football, league: Norwayn Toppserien women, équipe: Rosenborg BK Kvinner vs Arna-Bjornar et Rosenborg BK Kvinner gagne. remarque que l'equipe ou le joueur qui gagne est en fonction de la probabilité de gain 'away_percentage' ou 'home_percentage'.
 mais il est important que tu sois très court et concis donc ne fournis que des informations extremement nécessaires, evite s'il te plait de te presenté au debut.



'''
