import bs4
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from intro.models import Product


# Create your views here.


def index(request):
    return HttpResponse('Hello WORLD!')


def another_page(request):
    return HttpResponse('Hello Again!')


@login_required()
def cars(request):
    context = {
        'all_cars': [
            {
                'brand': 'Dacia',
                'color': 'black',
                'year': 2023,
                'is_new': False
            },
            {
                'brand': 'Volvo',
                'color': 'green',
                'year': 2024,
                'is_new': True
            },
            {
                'brand': 'BMW',
                'color': 'black',
                'year': 2021,
                'is_new': False
            }
        ]
    }

    return render(request, 'intro/list-cars.html', context)


@login_required()
def football(request):
    context = {
        'football_players': [
            {
                'name': 'Kylian Mbappe',
                'team': 'Real Madrid',
                'position': 'Forward',
                'contract_expire': 2029,
                'currently_playing': True
            },
            {
                'name': 'Toni Kroos',
                'team': 'Real Madrid',
                'position': 'Central Midfielder',
                'contract_expire': 2024,
                'currently_playing': False
            },
            {
                'name': 'Vinicius Junior',
                'team': 'Real Madrid',
                'position': 'Left Winger',
                'contract_expire': 2028,
                'currently_playing': True
            }
        ]
    }

    return render(request, 'intro/football-players.html', context)


def get_data(request):

    # Definim variabila in care stocam url
    url = 'https://www.emag.ro/laptopuri/c?ref=hp_menu_quick-nav_1_1&type=category'

    # Verificam daca cererea a fost cu success(200)
    response = requests.get(url)

    # Daca cererea este 200 (cu success)
    if response.status_code == 200:

        # Crearea unui obiect BeautifulSoup
        # response.content returneaza continutul din sursa paginii care este un html
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('div', class_='card-v2')
        list_articles = []

        for article in articles:
            name = article.find('a', class_='card-v2-title semibold mrg-btm-xxs js-product-url')
            price = article.find('p', class_='product-new-price')
            if name:
                print((name.text, price.text))
                list_articles.append((name.text, price.text))
            else:
                list_articles.append(('Titlu indisponibil', 'Pret indisponibil'))

        for element in list_articles:
            Product.objects.create(name=element[0], price=element[1])

    # Daca cererea NU este cu success printam un mesaj
    else:
        print(f'Eroare la accesarea paginii: {response.status_code}')
        return []

    return redirect('home_page')
