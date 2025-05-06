import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# Configurar opcions per a Chrome (incloent mode headless)
options = Options()
options.add_argument("--headless") # Executar sense obrir la finestra del navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# Obre una pàgina web

#Con esta variable le damos opcion al usuario de buscar en amazon lo que quiera
search = input("Que estas buscando: ")
driver.get(f"https://www.amazon.es/s?k={search}")

print("Títol de la pàgina:", driver.title)


#Espera a que cargue la pagina
time.sleep(1)

#Routa en la cual se guardara el html
route = r".\html\index.html" 

#Routa en la cual se guardara la info de los portatiles
file_route = r"info\info.json"

#Routa en la cual se guardaran las screenshots
screenshots = r"screenshots"

#-----------------------------------------------------------------------------------------------------------
# He tenido que usar Chat-Gpt para poder quitar las cookies. Lo siento <3
try:
    # Espera a que aparezca algún botón de cookies (hasta 10s)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='accept']"))
    )

    try:
        boton = driver.find_element(By.CSS_SELECTOR, "input[name='accept']")
        boton.click()
        print("Cookies aceptadas con input[name='accept']")
    except:
        try:
            boton = driver.find_element(By.ID, "sp-cc-accept")
            boton.click()
            print("Cookies aceptadas con ID sp-cc-accept")
        except:
            try:
                boton = driver.find_element(By.XPATH, "//input[@type='submit' and @name='accept']")
                boton.click()
                print("Cookies aceptadas con XPATH")
            except Exception as e:
                print("No se encontró el botón de cookies con ningún método:", e)

except Exception as e:
    print("No apareció el popup de cookies o ya estaba aceptado.")
# Esperar que la página cargue después de cerrar el popup
time.sleep(10)

#-----------------------------------------------------------------------------------------------------------


# Tomar la captura de pantalla y guardarla en la carpeta de screeshots
driver.save_screenshot(r".\screenshots\screenshot.png")


#Pasa el html a un archivo que se crea con el with open.
page_source = driver.page_source
with open (route, "w", encoding="utf-8") as f:
    f.write(page_source)
 
data = {'Title': [],'Link':[], 'Price':[], 'Stars':[], 'Delivery': []}

products = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")



#-----------------------------------------------------------------------------------------------------------
#Bucle para que nos enumere solo los 10 primeros productos
for i, product in enumerate(products[:10]): 
    
    titles= product.find_element(By.CSS_SELECTOR, "h2 span").get_attribute("innerHTML").strip() 
    #Capturamos los links de los prodcutos
    links = product.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal").get_attribute("href")
    
    try:
        #Capturamos el precio de los portatiles (euros, centimos y simbolo)
        coins =  product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        subcoins = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
        signs = product.find_element(By.CSS_SELECTOR, "span.a-price-symbol").text
        totalPrice = f"{coins}.{subcoins}{signs}"
    
    except:
        #Si no encuentra el precio o directamente no tiene precio muestra el siguiente mensaje.
        totalPrice = "Precio no disponible"
        
    
    try:
        #Capturamos las valoraciones de cada producto
        stars = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("innerHTML").strip() 
    except:
        #Si no encuentra ninguna valoración mandara el siguiente mensaje
        stars = "Sin valoraciones"
    
    
    try:
        #Capturamos la fecha de entrega  de los portatiles
        delivery = product.find_element(By.CSS_SELECTOR, "span.a-color-base.a-text-bold").get_attribute("innerHTML").strip()
        
    except:
        #Si no encuentra ninguna fecha de entrega mandara el siguiente mensaje
        delivery = "No hay fechas disponibles"
        
    try:
        #Capturamos imagenes de 10 primero productos y las guardamos en /screenshot
        img  = product.screenshot(f"./screenshots/screenshot_products/product_{i+1}.png")
        
    except:
        img = "No disponible"
        
    #Mostramos la información por terminal en forma de tabla    
    data['Title'].append(titles)
    data['Link'].append(links)
    data['Price'].append(totalPrice)
    data['Stars'].append(stars)
    data['Delivery'].append(delivery)
   #Para manejar errores que haya dentro del for al intentar buscar algun podructo 
    
   
 #-----------------------------------------------------------------------------------------------------------           

#Genera los datos en la consola de forma "bonita"
df = pd.DataFrame(data) 
print(df)

#Pasa df a json y lo pone en "file_route"
df.to_json(file_route, orient="records", indent=4)

#Sale de la pagina
driver.quit()