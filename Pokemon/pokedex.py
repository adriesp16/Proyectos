import requests


def infoPkmn(pokemon):

    #Función para la url
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    
    #Request a la url
    resposta = requests.get(url)

    if resposta.status_code == 200:
       
        dades = resposta.json()
        #Dentro de dades sacamos el "name" del "Pokemon"
        name = dades["name"]
        #Nos muestra el nombre por terminal
        print (f"\nName --> {name}\n")        
        #Dentro de dades sacamos el "numero de la pokedex" del "Pokemon"
        nPokedex = dades["id"]
        #Nos muestra el numero que ocupa en la pokedex por terminal
        print (f"nº Pokedex --> {nPokedex}\n")
        
        #Bucle nº1 para poder "sacar" la/as habilidad/es de un pokemon
        for i in range(len(dades["abilities"])):
            #Dentro de "abilities" nos metemos en "ability" y sacamos el "name" de esta
            ability = dades["abilities"][i]["ability"]["name"]
            #Mostramos por terminal "abilitie"
            print(f"Ability --> {ability}\n")
        
        #Bucle nº2 para "sacar" el/los tipo/os del pokemon
        for i in range(len(dades["types"])):
           #Dentro de "types" buscamos el "type" y dentro de este el "name"
           type =  dades["types"][i]["type"]["name"]
           #Mostramos por pantalla el "type"
           print(f"Type --> {type}\n")
        
        #Buscamos la img por delante del pokemon   
        img_normal_front = dades["sprites"]["front_default"]
        img_normal_back = dades["sprites"]["back_default"]

        #Buscamos la img por delante del pokemon en shiny
        img_shiny_front = dades["sprites"]["front_shiny"]
        img_shiny_back = dades["sprites"]["back_shiny"]
        #Mostramos el enlace de la imagen
        print(f"Img Normal Delante --> {img_normal_front}")
        print(f"Img Normal Detras --> {img_normal_back}\n")
        print(f"Img Shiny Delante --> {img_shiny_front}")
        print(f"Img Shiny Detras --> {img_shiny_back}")
        
    else:
        print("No se encuentra el pokemon")
#Nos pregunta cual es el pokemon que estamos buscando
infoPkmn(input("Que pokemon buscas? "))