import requests
import random
import json
import pprint


# Create your models here.
class Pokemon():
    api_url = 'https://pokeapi.co/api/v2/pokemon/'
    team_pool = []
    team_roster = []
    max_quantity = 905

    def __init__(self, name, types, sprite):
        self.name = name
        self.types = types
        self.sprite = sprite
    
    def newGame():
        Pokemon.clearData()
        Pokemon.getStarter()
        Pokemon.getTeam()
        
    def clearData():
        Pokemon.team_pool = []
        Pokemon.team_roster = []  
        
    def getStarter():
        rand_id = random.randint(1, Pokemon.max_quantity)
        starter_url = f'{Pokemon.api_url}{rand_id}'
        Pokemon.savePokemonData(starter_url, is_starter=True)

    def getTeam():
        for i in range(5):
            rand_index = random.randint(0, len(Pokemon.team_pool)-1)
            this_pokemon_url = Pokemon.team_pool[rand_index]['url']
            Pokemon.savePokemonData(this_pokemon_url)

    def savePokemonData(pokemon_url, is_starter=False):
        pokemon_data = requests.get(pokemon_url)
        pokemon = pokemon_data.json()

        name = Pokemon.getName(pokemon)
        sprite = Pokemon.getSprite(pokemon)

        if is_starter == True:
            types = Pokemon.getTypes(pokemon, is_starter=True)
        else:
            types = Pokemon.getTypes(pokemon)

        Pokemon.team_roster.append(
            Pokemon(name, types, sprite)
        )

    def makeTeamPool(types_urls):
        for url in types_urls:
            this_type_data = requests.get(url)
            this_type = this_type_data.json()

            for pokemon in this_type['pokemon']:
                this_url = pokemon['pokemon']['url'].split('/')
                if int(this_url[6]) <= Pokemon.max_quantity:
                    Pokemon.team_pool.append(pokemon['pokemon'])

    def getName(pokemon):
        name = pokemon['species']['name']
        return name.capitalize()

    def getSprite(pokemon):
        try:
            sprite = pokemon['sprites']['other']['official-artwork']['front_default']
        except:
            sprite = pokemon['sprites']['front_default']
        
        # if sprite == None:
        #     sprite = "{% static 'img/pokeball.png' %}"
        # else:
        return sprite

    def getTypes(pokemon, is_starter=False):
        types = []

        type1 = pokemon['types'][0]['type']['name']
        type1_url = pokemon['types'][0]['type']['url']
        types.append(type1)

        try:
            type2 = pokemon['types'][1]['type']['name']
            type2_url = pokemon['types'][1]['type']['url']
            types.append(type2)
        except:
            pass

        if is_starter == True:
            urls = []
            urls.append(type1_url)

            try:
                urls.append(type2_url)
            except:
                pass

            Pokemon.makeTeamPool(urls)

        return types
