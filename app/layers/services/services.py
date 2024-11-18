# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests 
def getAllImages(input=None):
    url = "https://rickandmortyapi.com/api/character/" # URL de la API de Rick & Morty para obtener personajes

    response = requests.get(url)  # Realizamos la solicitud GET a la API

    if response.status_code == 200: # Verificamos si la solicitud fue exitosa
        data = response.json()  # Convertimos la respuesta en formato JSON

        images = []
        for character in data['results']: # Iteramos sobre la lista de personajes en la respuesta de la API
            episode_url = character['episode'][0] # Obtenemos la URL del primer episodio del personaje
            
            # Realizamos una solicitud adicional para obtener los datos del episodio
            episode_response = requests.get(episode_url)
            episode_data = episode_response.json()
            
            # Obtenemos el nombre del episodio inicial
            episode_name = episode_data['name']  

            # Obtenemos la última ubicación del personaje
            last_location = character['location']['name']

            # Agregamos la informacion del personaje
            character_data = {
                'name': character['name'],  # Nombre del personaje
                'image': character['image'],  # URL de la imagen
                'status': character['status'],  # Estado del personaje (Alive, Dead, etc.)
                'last_location': last_location,  # Última ubicación conocida
                'episode_name': episode_name,  # Nombre del primer episodio donde aparece
            }
            
            # Agregamos el personaje a la lista
            images.append(character_data)

        return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.
