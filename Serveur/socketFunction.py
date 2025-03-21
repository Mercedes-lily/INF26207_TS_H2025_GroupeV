#Fonction liés aux sockets

import socket
import EnvoiServeur
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

# TODO :change to listen to client when connection is established
def loop_serveur(isconnect):
	while(isconnect == True):
		entreeClient = input(":> ").strip()
		entrerClientSplit = entreeClient.split(" ")
		if(entrerClientSplit[0] == "open"):
			print("Veuillez fermer la connection avec le serveur en cours avec la commande bye")
		if(entrerClientSplit[0] == "bye"and len(entrerClientSplit[0]) == 1):
			isconnect = False
			commandeBye()
		elif(entrerClientSplit[0] == "bye"and len(entrerClientSplit[0]) != 1):
			print("Veuillez entrer la commande bye uniquement")
		if(entrerClientSplit[0] == "get"and len(entrerClientSplit[0]) == 2):
			commandeGet()
		elif(entrerClientSplit[0] == "get"and len(entrerClientSplit[0]) != 2):
			print("Veuillez entrer la commande open et une unique adresse ip")
		if(entrerClientSplit[0] == "ls" and len(entrerClientSplit[0]) == 1):
			commandeLs()
		elif(entrerClientSplit[0] == "ls"and len(entrerClientSplit[0]) != 1):
			print("Veuillez entrer la commande ls uniquement")
		else:
			print("Entrer une commande valide parmis get pour obtenir un fichier, bye pour fermer la connexion avec le serveur ou ls pour obtenir la liste des fichier disponible au téléchargement")


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
		return False #pas le bon syn ou ack
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
	print("nego done")
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
	try:
		print("3 way : nouveau")
		serv_socket.settimeout(0.1)
		tried = 0
		while True:
			try:
				data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
				if not data or tried > 4:
					break  #TODO Connexion fermée par l'hôte distant ############UTILE? 
				message = data.decode()
				print(f"Received data from {client_adresse}: {message}")
				if negociation(message, conf, "SYN") == True:
					print("tried: " + str(tried))
					print("negociation")
					serv_socket.settimeout(3)
					message = CreateThreeWayHeader("SYN-ACK\r\n", conf)
					tried += 1
					if EnvoiServeur.canSend():
						serv_socket.sendto(message.encode(), client_adresse)
					else:
						print("Erreur envoie")
				elif negociation(message, conf, "ACK") == True:
					data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
					print(f"Received data from {client_adresse}: {data.decode()}")
					if(data.decode() == "ls\r\n"):
						handle_ls_command(client_adresse, serv_socket)
					if(data.decode() == "bye\r\n"):
						handle_bye_command(client_adresse, serv_socket)
			except socket.timeout:
				pass  # Ignorer les délais d'attente et continuer
	except KeyboardInterrupt:
		print("3 way : Echec (Ctrl+C)")

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
	threeWay(conf, serv_socket)
	return serv_socket 

