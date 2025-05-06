import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)

route = r'C:\Users\Adrian\Documents\Ejercicios programación\python2\scraping-web\file1.txt'


if response.status_code == 200:
    html = response.text
else:
    print(f"Error en accedir a la pagina: {requests.status_code}")
    
soup = BeautifulSoup(html, "html.parser")

items = soup.find_all("div", class_= "country")

data = {'País': [], 'Población': [], 'Área': []}

with open(route, "w", encoding= "utf-8") as file:
    for item in items:    
        pais = item.find('h3', class_='country-name').text.strip() #Encuentra el nombre del país y lo guarda en la variable country_name
        population = item.find('span', class_='country-population').text.strip() #Encuentra el numero de la población y lo guarda en la variable population
        area = item.find('span', class_='country-area').text.strip() #Encuentra el nombre area en km² y lo guarda en la variable area
        
        data["País"].append(pais)
        data["Población"].append(int(population))
        data["Área"].append(float(area))
        file.write(f" País: {pais}\n Población: {population}\n Área (km²):{area}\n  -------------- \n") #Escribe los datos almacenados de las variables en el file1.txt
 
df = pd.DataFrame(data) #Genera los datos en la consola de forma "bonita"
print(df)