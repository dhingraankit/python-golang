from bs4 import BeautifulSoup
import requests
import urllib
import re
import csv

def makeUrl(link):
    if link.startswith('/store'):
        return "https://play.google.com" + link
    else:
        return link
    
    
def getMail(search_email):
    if len(search_email) > 0:
        for i in range(0, len(search_email)):
            if search_email[i].has_attr('href') and "mailto" in search_email[i]['href']:
                publisher_email = search_email[i]['href'].replace("mailto:","")
                return publisher_email

            
def getGameDetails(gamelink):
    
    gameDetails = ["NA","NA","NA","NA","NA","NA","NA","NA","NA"]
    game_page = requests.get(gamelink)
    game_page_xml = BeautifulSoup(game_page.text, 'html.parser')
    
    gameDetails[0] = gamelink

    if len(game_page_xml) > 0:
        #Searching for Game Name    
        game_name = game_page_xml.find_all('h1')
        if len(game_name) > 0:
            game_name_2 = game_name[0].text.replace(",","")
            #print(game_name)
            gameDetails[1] = game_name_2
    
        #Searching for Game Genre    
        search_genre = game_page_xml.find_all('a', itemprop="genre")
        if len(search_genre) > 0:
            game_genre = search_genre[0].text
            #print(game_genre) s
            gameDetails[2] = game_genre
    
        #Searchin for publisher name    
        search_publisher = game_page_xml.find_all('a', class_="hrTbp R8zArc")
        if len(search_publisher) > 0:
            game_publisher = search_publisher[0].text
            #print(game_publisher)
            gameDetails[3] = game_publisher
    
    
        #Searching for Publisher Email    
        search_email = game_page_xml.find_all('a', class_="hrTbp")
        if len(search_email) > 0:
            if getMail(search_email) is not None:
                publisher_email_id = getMail(search_email)
                #print(publisher_email_id)
                gameDetails[4] = publisher_email_id  
    
    
        #Searching for Game Size
        search_size = game_page_xml.find_all('div', class_="xyOfqd")
        if len(search_size) > 0:
            for i in range(len(search_size)):
                sub_search_size = search_size[0].find_all('div', class_="hAyfc")
                if len(sub_search_size) > 0:
                    for value in sub_search_size:
                        if "Size" in value.find('div', class_="BgcNfc").text:
                            size = value.find('span', class_="htlgb").text
                            #print(size)
                            gameDetails[5] = size
    

        #Searching for game Last Update Date
        search_date = game_page_xml.find_all('div', class_="xyOfqd")
        if len(search_date) > 0:
            for i in range(len(search_date)):
                sub_search_date = search_date[0].find_all('div', class_="hAyfc")
                if len(sub_search_date) > 0:
                    for value in sub_search_date:
                        if "Updated" in value.find('div', class_="BgcNfc").text:
                            date = value.find('span', class_="htlgb").text
                            #print(date)
                            gameDetails[6] = date.replace(',','')
    
    
        #Searching for Installs
        search_installs = game_page_xml.find_all('div', class_="xyOfqd")
        if len(search_installs) > 0:
            for i in range(len(search_installs)):
                sub_search_installs = search_installs[0].find_all('div', class_="hAyfc")
                if len(sub_search_installs) > 0:
                   for value in sub_search_installs:
                        if "Installs" in value.find('div', class_="BgcNfc").text:
                            installs = value.find('span', class_="htlgb").text
                            installs_2 = installs.replace('+','')
                            #print(date)
                            gameDetails[7] = installs_2.replace(',','')           
    
    
        #Searching for Website
        search_website = game_page_xml.find_all('a', class_="hrTbp")
        if len(search_website) > 0:
            for i in range(0, len(search_website)):
                if search_website[i].has_attr('href') and "Visit website" in search_website[i].text:
                    website = search_website[i]['href']
                    gameDetails[8] = website.replace(',','')         
            
    return gameDetails


#Getting Similar apps link from a game page
def getSimilarLink(gamelink):
    random_request = requests.get(gamelink)
    random_xml = BeautifulSoup(random_request.text, 'html.parser')
    search_see_more = random_xml.find_all('div', class_="g4kCYe")
    if len(search_see_more) > 0:
        sub_search_more = search_see_more[0].find_all('a',class_="LkLjZd ScJHi IfEcue nMZKrb id-track-click ")
        if len(sub_search_more) > 0:
            similar_link = sub_search_more[0]['href']
            return similar_link


#Getting all game link from the similar games page in a list        
def getGames(See_more_link):
    random_request = requests.get(See_more_link)
    random_xml = BeautifulSoup(random_request.text, 'html.parser')
    search_games = random_xml.find_all('div', class_="id-card-list card-list two-cards")
    similar_links = []
    if len(search_games) > 0:
        sub_search_games = search_games[0].find_all('a', class_="title")
        for i in range(len(sub_search_games)):    
            if sub_search_games[i].has_attr('href'):
                Gamelink = makeUrl(sub_search_games[i]['href'])
                similar_links.append(Gamelink)
    return similar_links

#Declaring this list of games as seed nodes
def read_csv(csv_name,command):
    f1 = open(csv_name, command)
    c1 = csv.reader(f1)
    masterlist = list(c1)
    already_done = []
    for value in masterlist:
        new = value[0]
        already_done.append(new)
    return already_done

already_done_emails = read_csv('Email_Master.csv', 'r')

DoneLinks = []

#Seed list of games
SeedLinks = ['https://play.google.com/store/apps/details?id=com.playappking.spiderboy']

#Starting node number
seed_count = 0

#Max Number of nodes to iterate
max_nodes = 10

#While current node is lesser than max nodes
with open("ps_scrapper_v2.csv", "w") as csv_file: 
    while seed_count <= max_nodes:
        PendingLinks = []
        for game in SeedLinks:
            try:
                #getting a game details done
                gameDone = getGameDetails(game)
                if gameDone[4] not in already_done_emails:
                    csv_file.write(','.join(gameDone) + '\n')
                    DoneLinks.append(game)
                    print("Done Links: ", len(DoneLinks))
                    
                    #Getting see more link on every game
                    see_more = getSimilarLink(game)
                    
                    #Going to see more page to 
                    games_links = getGames(see_more)
                    for value in games_links: 
                        if value not in DoneLinks and value not in PendingLinks:
                            PendingLinks.append(value)
                        else:
                            continue 
                else:
                    continue
            except requests.exceptions.MissingSchema:
                continue 
        seed_count = seed_count + 1
        print("Nodes Completed: ", seed_count)                         
        print("Pending Links: ", len(PendingLinks))
        
        #Assigning Pending links to Seedlinks for the next iteration
        SeedLinks = PendingLinks