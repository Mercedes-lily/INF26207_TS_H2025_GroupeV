#Fichier contenant les fonctions liées au fonctionnalité du serveur
import os

#Endroit où sont stocké les fichiers à télécharger
FILES_DIRECTORY = "Serveur/server_files"

#Fonction qui retourne les fichiers disponibles dans le répertoire spécifié
def list_files():
     if not os.path.exists(FILES_DIRECTORY):
         os.makedirs(FILES_DIRECTORY)  # Créer le répertoire s'il n'existe pas
     files = os.listdir(FILES_DIRECTORY)
     return files

# Fonction pour gérer la commande "ls"
def handle_ls_command(client_address, serv_socket):
    files = list_files()
    if not files:
        response = "Aucun fichier disponible."
    else:
        response = "Fichiers disponibles:\n" + "\n".join(files)
    serv_socket.sendto(response.encode(), client_address)
    print(f"Liste des fichiers envoyée au client {client_address}" + response)

# Fonction pour gérer la commande "bye" - Déconnexion
def handle_bye_command(client_address, serv_socket):
    response = "bye\r\n"
    serv_socket.sendto(response.encode(), client_address)

# Fonction pour gérer la commande "get" - Envoie de fichier
def handle_get_command():
    return 0