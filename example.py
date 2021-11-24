from bs4 import BeautifulSoup
import requests
import openpyxl

# Excel that que contains information of 40000 movies
excel_document = openpyxl.load_workbook('MovieGenreIGC_v3.xlsx')
page = excel_document.active
# print(page['B2'].value)
page.max_column
url_list = []
url_http = "http://www.imdb.com/title/tt"
for i in range(2, 15):
    seed = page.cell(row = i, column = 1).value

    full_seed = str(seed).zfill(7)
    full_url = url_http + full_seed 
    url_list.append(full_url)


for i in range(0, len(url_list)):
    response = requests.get(url_list[i])
    soup = BeautifulSoup(response.text, 'html.parser')

    # name_box = soup.title.string
    # Obtención del título en castellano
    name_box = soup.find('h1', attrs={'data-testid': 'hero-title-block__title'}).get_text()
    # Obtención del título original (en su idioma original)
    original_title = soup.find('div', attrs={'data-testid': 'hero-title-block__original-title'})

    genres = soup.find('div', attrs={'data-testid': 'genres'}).find_all('span', attrs={'class': 'ipc-chip__text'})
    genres_list = []
    
    for i in range(len(genres)):
        genres_list.append(genres[i].get_text())
    print("Genres ", genres_list)
    if(original_title is not None):
        original_title = original_title.get_text().split(': ')
        print(str(name_box) + " original title: " + str(original_title[1]))
    else:
        print(str(name_box) )

    # print(name_box)
    
    #print('-----------------------------------')
    
# name_box = soup.find('h1', attrs={'class': 'TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG'}).get_text()
# print(name_box)
# '''print(soup.find_all(class_h1))'''