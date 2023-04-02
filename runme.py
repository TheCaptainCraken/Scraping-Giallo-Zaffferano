import json
import requests
from scrape_schema_recipe import scrape_url
from bs4 import BeautifulSoup
from time import sleep
from random import random
import os

BASE_URL = 'https://www.giallozafferano.it/ricette-cat/page'

# Creates a JSON file containing the datefound in a recipe page of Giallo Zafferano.
# If a piece of data is mising on the website, the corresponding field in the JSON object returned will be null.
# If the request fails, the code will inform the user, wait 10 seconds and then continue.


def create_recipe(url):
    try:
        recipe = scrape_url(url)[0]  # This might fail
    except:
        print(f'An error has occured while scraping recipe @ {url}')
        # Maybe this is optional as I am not sure if the website has a limitation on the number of requests.
        sleep(10)
        return
    # The file names will have spaces and non ASCII charachters.
    file_name = recipe['name'].lower()

    data = {}

    keys = recipe.keys()

    # Saving all useful data and changing key names for ease of use later.
    # This part is tedius beacuse there is no guarantee that any field is present in the original data.

    data['nome'] = recipe['name'] if 'name' in keys else None
    data['costo'] = recipe['estimatedCost'] if 'estimatedCost' in keys else None
    data['categoria'] = recipe['recipeCategory'] if 'recipeCategory' in keys else None
    data['url_immagine'] = recipe['image'] if 'image' in keys else None
    data['descrizione'] = recipe['description'] if 'description' in keys else None
    data['numero_porzioni'] = recipe['recipeYield'] if 'recipeYield' in keys else None
    data['ingredienti'] = recipe['recipeIngredient'] if 'recipeIngredient' in keys else None
    data['istruzioni'] = recipe['recipeInstructions'] if 'recipeInstructions' in keys else None
    data['keywords'] = recipe['keywords'] if 'keywords' in keys else None
    data['metodo_cottura'] = recipe['cookingMethod'] if 'cookingMethod' in keys else None
    data['tempo_preparazione'] = recipe['prepTime'] if 'prepTime' in keys else None
    data['tempo_cottura'] = recipe['cookTime'] if 'cookTime' in keys else None
    data['tempo_totale'] = recipe['totalTime'] if 'totalTime' in keys else None

    if 'aggregateRating' in keys:
        data['statistiche'] = {}
        secondary_keys = recipe['aggregateRating'].keys()
        if 'ratingCount' in secondary_keys:
            data['statistiche']['votazioni_utenti'] = recipe['aggregateRating']['ratingCount']
        else:
            data['statistiche']['votazioni_utenti'] = None
        if 'ratingValue' in secondary_keys:
            data['statistiche']['voto_medio'] = recipe['aggregateRating']['ratingValue']
        else:
            data['statistiche']['voto_medio'] = None
    else:
        data['statistiche'] = None

    if 'video' in keys:
        tertiary_keys = recipe['video'].keys()
        if 'contentUrl' in tertiary_keys:
            data['url_video'] = recipe['video']['contentUrl']
        else:
            data['url_video'] = None
    else:
        data['url_video'] = None

    # Saves the data just created in the 'ricette' folder.
    with open(f'ricette/{file_name}.json', 'w') as file:
        file.write(json.dumps(data))

# Returns the number of result pages in the website's own search page.
# Every result page contains ~15 recipes. At the time of writing there are a little over 6400 recipes in total.


def countTotalPages():
    numberOfPages = 0
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    for tag in soup.find_all(attrs={'class': 'disabled total-pages'}):
        numberOfPages = int(tag.text)
    return numberOfPages


# This function wil download every recipe and save it in a JSON format in a folder names 'ricette'.
# If the function can't fetch a results page it will inform the user, wait 10 seconds and the skip to the next results page.
# If the function can't fetch a single recipe then it will also inform the user, wait 10 seconds and skip that recipe.
def downloadAllRecipesFromGialloZafferano():
    try:
        os.mkdir('ricette')
    except FileExistsError:
        pass  # The folder already exists: nothing more has to be done.

    for pageNumber in range(1, countTotalPages() + 1):
        result_page_url = BASE_URL + str(pageNumber)
        try:
            response = requests.get(result_page_url)  # This might fail.
        except:
            print(
                f'an error has occured while scraping search page # {pageNumber}')
            sleep(10)
            continue
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        # Gets all the links to recipe pages in a single results page.
        for tag in soup.find_all(attrs={'class': 'gz-title'}):
            link = tag.a.get('href')
            create_recipe(link)
            # This might be optional. I tried without but I got way more misses. This seems to be the perfect waiting time for me.
            sleep(random() * 3)


# LET'S GOOOOOOO
downloadAllRecipesFromGialloZafferano()
