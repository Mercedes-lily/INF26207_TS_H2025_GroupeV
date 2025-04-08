#Fichier contenant les fonctions liées au fonctionnalité du serveur
import os
import Header
import EnvoiServeur

#Endroit où sont stocké les fichiers à télécharger
FILES_DIRECTORY = "Serveur/server_files"

#Fonction qui retourne les fichiers disponibles dans le répertoire spécifié
def list_files():
	if not os.path.exists(FILES_DIRECTORY):
		os.makedirs(FILES_DIRECTORY)  # Créer le répertoire s'il n'existe pas
	files = os.listdir(FILES_DIRECTORY)
	return files

# Fonction pour gérer la commande "ls"
def handle_ls_command(client_address, serv_socket, conf):
	files = list_files()
	response = Header.CreateLsHeaderServeur(files)
	if EnvoiServeur.canSend(float(conf["Fiabilite"])):
		serv_socket.sendto(response.encode(), client_address)
		print(f"Liste des fichiers envoyée au client {client_address} \n" + response)

# Fonction pour gérer la commande "bye" - Déconnexion
def handle_bye_command(client_address, serv_socket, conf):
	response = Header.CreateByeHeaderServeur()
	if EnvoiServeur.canSend(float(conf["Fiabilite"])):
		serv_socket.sendto(response.encode(), client_address)

# Fonction qui permet de segmenter en morceau les donnees du fichier à envoyer 
def segmentation(file, conf):
	segments = []
	f = open(FILES_DIRECTORY + "/" + file, "rb")
	while True:
		seg = f.read(int(conf["DataSize"]) - 100)  # -100 pour le header
		if seg:
			segments.append(seg)
		else:
			break
	f.close()
	return segments

#Fonction qui permet d'envoyer les segments de fichier au client et d'attendre la confirmation
def sendToClient(file_segmented, client_adresse, serv_socket, conf):
	j = 0
	BlocConfirmation = int(conf["DataConfirmation"])
	tried = 0
	nbSegment = len(file_segmented)
	serv_socket.settimeout(3)
	while tried < 5:
		try:
			#Boucle d'envoie du nombre de segment spécifié dans le fichier de configuration
			for i in range(0, BlocConfirmation, 1):
				if j < nbSegment:
					if EnvoiServeur.canSend(float(conf["Fiabilite"])):
						serv_socket.sendto(file_segmented[j], client_adresse)
						print(f"Envoi du segment {j}/{nbSegment - 1} au client {client_adresse}")
					j+= 1
				else:
					break
			#Attente de la confirmation du client
			data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))
			if data.decode().split("\r\n")[0] == "Confirmation":
				if j == nbSegment:
					serv_socket.settimeout(0.1) # On remet le timeout à 0.1 pour que le serveur soit réactif au ctrl+c
					return
				else:
					tried = 0
			else:
				j -= BlocConfirmation
				if j < 0:
					j = 0
				tried += 1
		except Exception as e:
			print(f"Erreur de réception de la confirmation: {e} ({tried})")
			if tried < 5:
				tried += 1
				j-= BlocConfirmation
				if j < 0:
					j = 0
			else:
				print("Le client ne répond pas, arrêt de l'envoi.")
				message = Header.CreateEchecHeaderServeur()
				if EnvoiServeur.canSend(float(conf["Fiabilite"])):
					serv_socket.sendto(message.encode(), client_adresse)
				break
	serv_socket.settimeout(0.1)

# Fonction pour gérer la commande "get" - Envoie de fichier
def handle_get_command(data, client_adresse, serv_socket, conf):
	files = list_files()
	print(f"file to get : {data.decode()}")
	found = False
	for file in files:
		if file in data.decode(): # Vérifie si le fichier demandé est dans la liste
			print(f"file found : {file}")
			found = True
			file_segmented = segmentation(file, conf)
			for i in range(0, len(file_segmented), 1):
				if i != len(file_segmented) - 1:
					file_segmented[i] = Header.CreateGetHeaderServeur(file, "False", file_segmented[i], i)
				else:
					file_segmented[i] = Header.CreateGetHeaderServeur(file, "True", file_segmented[i], i)
			sendToClient(file_segmented, client_adresse, serv_socket, conf)
	if not found:
		print("File not found.")
		message = Header.FileNotFoundHeaderServeur()
		if EnvoiServeur.canSend(float(conf["Fiabilite"])):
			serv_socket.sendto(message.encode(), client_adresse)
	return False
