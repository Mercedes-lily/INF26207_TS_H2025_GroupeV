#Fonction liés aux sockets

import socket
import Envoie
import os

# Répertoire où les fichiers sont stockés
FILES_DIRECTORY = "Serveur/server_files"
# Fonction pour lister les fichiers disponibles

#Fichier contenant les fonctions liées au fonctionnalité du serveur

# ls : Le client demande la liste des fichiers disponibles sur le serveur.

 #Le serveur doit être capable de lister les fichiers disponibles dans un répertoire spécifique et de les envoyer au client.
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
    # Envoyer la réponse au client

def handle_bye_command(client_address, serv_socket):
    response = "bye\r\n"
    serv_socket.sendto(response.encode(), client_address)

def negociation(message, conf, SYNACK):   # regarder le SYN
    splitmessage = message.split("\r\n")
    if(splitmessage[0] != SYNACK):
        print("pas le bon syn ou ack")
        return False
    dataRecu = {}
    for m in splitmessage:
        splitm = m.split(":")
        if len(splitm) == 1:
            continue
        dataRecu[splitm[0]] =  splitm[1]
    if(int(dataRecu["TailleHeader"]) != len(message)):
        print("difference de taille")
        return False
    if(conf["DataSize"] != dataRecu["Taille"]):
        conf["DataSize"] = dataRecu["Taille"]
    if(conf["DataConfirmation"] > dataRecu["NombreMorceaux"]):
        conf["DataConfirmation"] = dataRecu["NombreMorceaux"]
    return True

def CreateThreeWayHeader(message, conf) :
    message += "Taille:"+ conf["DataSize"].strip() + "\r\n"
    message += "NombreMorceaux:" + conf["DataConfirmation"].strip() + "\r\n"
    tailleheader = len(message) + len("TailleHeader:") + 4
    tailleheader += len(str(tailleheader))
    message += "TailleHeader:" + str(tailleheader) + "\r\n"
    message += "\r\n"
    return message

#reste le temps dattente et aussi le retourner si le ack nest pas satisfait
def threeWay(conf, serv_socket):
    data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
    message = data.decode()
    print(f"Received data from {client_adresse}: {message}")
    if negociation(message, conf, "SYN") == True:
        print("negociation")
        serv_socket.settimeout(5)
        message = CreateThreeWayHeader("SYN-ACK\r\n", conf)
        serv_socket.sendto(message.encode(), client_adresse)
    data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
    message = data.decode()
    print(f"Received data from {client_adresse}: {data.decode()}")
    if negociation(message, conf, "ACK") == True:
        data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
        print(f"Received data from {client_adresse}: {data.decode()}")
        if(data.decode() == "ls\r\n"):
            handle_ls_command(client_adresse, serv_socket)
        if(data.decode() == "bye\r\n"):
            handle_bye_command(client_adresse, serv_socket)


        
        

        





# code proprement dit :







# AUTRE CHOSE

# import socket

# # Configuration du client
# SERVER_HOST = '127.0.0.1'  # Adresse IP du serveur (localhost par défaut)
# SERVER_PORT = 2212         # Port du serveur
# BUFFER_SIZE = 1024         # Taille du buffer pour recevoir les données

# # Création du socket UDP
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# def send_command(command):
#     """
#     Envoie une commande au serveur et attend la réponse.

#     :param command: La commande à envoyer (par exemple, "open 127.0.0.1", "ls", "get fichier.txt", "bye").
#     """
#     # Envoyer la commande au serveur
#     client_socket.sendto(command.encode(), (SERVER_HOST, SERVER_PORT))
#     print(f"Commande envoyée au serveur : {command}")

#     # Attendre la réponse du serveur
#     try:
#         client_socket.settimeout(5)  # Timeout de 5 secondes pour la réponse
#         data, server_address = client_socket.recvfrom(BUFFER_SIZE)
#         print(f"Réponse du serveur {server_address}: {data.decode()}")
#     except socket.timeout:
#         print("Timeout : Aucune réponse du serveur.")

# def open_command(ip_address):
#     """
#     Envoie une commande "open" au serveur pour initier une connexion.

#     :param ip_address: Adresse IP du serveur.
#     """
#     send_command(f"open {ip_address}")

# def ls_command():
#     """
#     Envoie une commande "ls" au serveur pour demander la liste des fichiers disponibles.
#     """
#     send_command("ls")

# def get_command(filename):
#     """
#     Envoie une commande "get" au serveur pour demander un fichier spécifique.

#     :param filename: Le nom du fichier à télécharger.
#     """
#     send_command(f"get {filename}")

# def bye_command():
#     """
#     Envoie une commande "bye" au serveur pour terminer la connexion.
#     """
#     send_command("bye")










# try:
#         serv_socket.settimeout(0.1)
#         tried = 0
#         while True:
#             try:
#                 data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
#                 if not data:
#                     break  # Connexion fermée par l'hôte distant
#                 data_decode = data.decode()
#                 print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
#                 if data_decode == "SYN" or (tried <= 5 and data_decode != "ACK"):
#                     serv_socket.settimeout(3)
#                     message = "SYN-ACK"
#                     if Envoie.canSend():
#                         tried += 1
#                         serv_socket.sendto(message.encode(), client_adresse)
#                 elif data.decode() == "ACK":
#                     print("3 way : reussi")
#                     return serv_socket
#             except socket.timeout:
#                 pass  # Ignorer les délais d'attente et continuer
#     except KeyboardInterrupt:
#         print("3 way : Echec (Ctrl+C)")
    
# # data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
# #         data_decode = data.decode()
# #         print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
# #         if data_decode == "SYN":
# #             serv_socket.settimeout(5)
# #             message = "SYN-ACK"
# #             if Envoie.canSend():
# #                 serv_socket.sendto(message.encode(), client_adresse)
# #         data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
# #         print(f"Received data from {client_adresse}: {data.decode()}") #decodes the recieved bytes.
# #         if data.decode() == "ACK":
# #             print("3 way : reussi")
#         # return serv_socket
#Initialisation du socket UDP du côté serveur et implémentation du three-Way Handshake
#Lecture necessaire dans un fichier de configuration
def ServeurStart(conf):
    port = 2212
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        serv_socket.bind((conf["IPv4"], port))
        print("Bind : Succes")
    except Exception as e:
        print("Bind : Echec, error: " + e)
        exit()
    serv_socket.settimeout(10)
    threeWay(conf, serv_socket)

    return serv_socket 

