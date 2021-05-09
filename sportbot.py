from pywikiapi import Site

site = Site('http://wikipast.epfl.ch/wikipast/api.php') # Définition de l'adresse de l'API
site.no_ssl = True # Désactivation du https, car pas activé sur wikipast
site.login("User@Name", "Password") # Login du bot