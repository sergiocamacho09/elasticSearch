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

    name_box = soup.title.string

    print(name_box)
    print('-----------------------------------')

# name_box = soup.find('h1', attrs={'class': 'TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG'}).get_text()
# print(name_box)
# '''print(soup.find_all(class_h1))'''