from bs4 import BeautifulSoup
import requests
import openpyxl
import json

# Excel that que contains information of 40000 movies
excel_document = openpyxl.load_workbook('MovieGenreIGC_v3.xlsx')
page = excel_document.active
# print(page['B2'].value)
page.max_column
url_list = []
plot_url_list = []
cast_url_list = []
keywords_url_list = []
url_http = "http://www.imdb.com/title/tt"
plot_to_go = "/plotsummary?ref_=tt_ov_pl"
full_cast_to_go = "/fullcredits?ref_=tt_ov_st_sm"
keywords_to_go = "/keywords?ref_=tt_stry_kw"
cast_list = []
keywords_list = []

for i in range(2, 15):
    seed = page.cell(row = i, column = 1).value
    full_seed = str(seed).zfill(7)
    full_url = url_http + full_seed 
    url_list.append(full_url)
    

for i in range(0, len(url_list)):
    screenwriters_list = []
    genres_list = []
    language_list = []
    
    plot_url_list.append(url_list[i] + plot_to_go)
    cast_url_list.append(url_list[i] + full_cast_to_go)
    keywords_url_list.append(url_list[i] + keywords_to_go)
    response = requests.get(url_list[i])
    response2 = requests.get(plot_url_list[i])
    response3 = requests.get(cast_url_list[i])
    respones4 = requests.get(keywords_url_list[i])
    soup = BeautifulSoup(response.text, 'html.parser')
    plot_soup = BeautifulSoup(response2.text, 'html.parser')
    cast_soup = BeautifulSoup(response3.text, 'html.parser')
    keywords_soup = BeautifulSoup(respones4.text, 'html.parser')

    # name_box = soup.title.string
    # Obtención del título en castellano
    name_box = soup.find('h1', attrs={'data-testid': 'hero-title-block__title'}).get_text()
    # Obtención del título original (en su idioma original)
    original_title = soup.find('div', attrs={'data-testid': 'hero-title-block__original-title'})

    # Obtención de los generos de cada uno de las películas
    genres = soup.find('div', attrs={'data-testid': 'genres'}).find_all('span', attrs={'class': 'ipc-chip__text'})
  
    
    # Obtención del año de estreno de cada una de las películas
    year = soup.find('span', attrs={'class': 'TitleBlockMetaData__ListItemText-sc-12ein40-2'}).get_text()
    #Obtención del rating de la película
    rating = soup.find('span', attrs={'class' :'AggregateRatingButton__RatingScore-sc-1ll29m0-1'}).get_text()
    #Obtemción del argumento de la pelicula (lo consultamos en una página a la que se nos redirecciona)
    plot = plot_soup.find('ul', attrs={'id' :'plot-summaries-content'}).find('p').get_text()

    # Obtención del reparto completo de la película (todos sus actores)
    cast_list = cast_soup.find('table', attrs={'class': 'cast_list'}).find_all('td', attrs={'class': ''})

    # Obtención del director/es de la película
    director = cast_soup.find_all('table', attrs={'class' : 'simpleCreditsTable'})[0].find('td', attrs={'class' : 'name'}).get_text()

    #Obtencion de los guionistas de la pelicula
    screenwriters = cast_soup.find_all('table', attrs={'class' : 'simpleCreditsTable'})[1].find_all('td', attrs={'class' : 'name'})

    #Palabras clave de la pelicula
    keywords_list = keywords_soup.find('table', attrs={'class' : 'evenWidthTable2Col'}).find_all('div', attrs={'class' : 'sodatext'})

    #idioma de la película
    language = soup.find('li', attrs={'data-testid': 'title-details-languages'}).find_all('a', attrs={'class': 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
    # Mostramos todos los datos por pantalla para mostrar
    for i in range(len(language)):
        if(language[i].get_text() != "None"):
            language_list.append(language[i].get_text())

    #MIRAR POR QUÉ NO FUNCIONA EL IF
    print('-----------------------------------')
    print("Languages: " , language_list)

    for i in range(len(genres)):
        genres_list.append(genres[i].get_text())
    print("Genres ", genres_list)

    for i in range(len(cast_list)):
        print(cast_list[i].get_text())

    for i in range(len(screenwriters)):
        screenwriters_list.append(screenwriters[i].get_text().replace("\n", ""))

    for i in range(len(keywords_list)):
        print(keywords_list[i].get_text())

    if(original_title is not None):
        original_title = original_title.get_text().split(': ')
        print(str(name_box) + " | original title: " + str(original_title[1]) + " | year: " + str(year) + " | rating: " + str(rating))
        print("Director: " + str(director))
        print("ScreenWriters: " + str(screenwriters_list))
        print(plot)
    else:
        print(str(name_box) + " | year: " + str(year) + " | rating: " + str(rating))
        print("director: " + str(director))
        print("screenwriters: " + str(screenwriters_list))
        print(plot)
    
    print('-----------------------------------')
    
