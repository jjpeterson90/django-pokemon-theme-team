from django.http import HttpResponse
from django.shortcuts import render
from .models import Pokemon
import requests
import pprint


# Create your views here.
def index(request):
    print(request.method)
    if request.method == "POST":
        Pokemon.newGame()
    
        paired_list = []
        for i in range(0, len(Pokemon.team_roster)-1, 2):
            paired_list.append([Pokemon.team_roster[i], Pokemon.team_roster[i+1]])
        
        data = {
            'pokemon_pairs': paired_list,
        }
        
        return render(request, 'pages/team.html', data)

    return render(request, 'pages/home.html')