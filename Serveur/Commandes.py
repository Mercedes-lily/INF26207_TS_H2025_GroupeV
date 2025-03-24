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
def handle_ls_command(client_address, serv_socket):
	files = list_files()
	response = Header.CreateLsHeaderServeur(files)
	serv_socket.sendto(response.encode(), client_address)
	print(f"Liste des fichiers envoyée au client {client_address} \n" + response)

# Fonction pour gérer la commande "bye" - Déconnexion
def handle_bye_command(client_address, serv_socket):
	response = Header.CreateByeHeaderServeur()
	serv_socket.sendto(response.encode(), client_address)

def segmentation(file, conf):
	segments = []
	f = open(FILES_DIRECTORY + "/" + file, "rb")
	while True:
		seg = f.read(int(conf["DataSize"]))
		if seg:
			segments.append(seg)
		else:
			break
	f.close()
	return segments

def sendToClient(file_segmented, client_adresse, serv_socket, conf):
	j = 0
	serv_socket.settimeout(3)
	while True:
		for i in range(0, int(len(conf["DataConfirmation"])), 1):
			if j < len(file_segmented):
				if EnvoiServeur.canSend():
					serv_socket.sendto(file_segmented[j], client_adresse)
					print(f"Envoi du segment {j} au client {client_adresse}")
				j+= 1
			else:
				break
		try:
			data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))
			print(f"Réponse du client {client_adresse}: {data.decode()}")
			if data.decode() == "RECEIVED":
				continue
			else:
				j -= 4
		except Exception as e:
			print(f"Erreur de réception: {e}")
			break
	serv_socket.settimeout(0.1)

# Fonction pour gérer la commande "get" - Envoie de fichier
def handle_get_command(data, client_adresse, serv_socket, conf):
	files = list_files()
	print(f"file to get : {data.decode()}")
	for file in files:
		if file in data.decode(): # Vérifie si le fichier demandé est dans la liste
			print(f"file found : {file}")
			file_segmented = segmentation(file, conf)
			for i in range(0, len(file_segmented), 1):
				if i != len(file_segmented) - 1:
					file_segmented[i] = Header.CreateGetHeaderServeur(file, "False", file_segmented[i], i)
				else:
					file_segmented[i] = Header.CreateGetHeaderServeur(file, "True", file_segmented[i], i)
			sendToClient(file_segmented, client_adresse, serv_socket, conf)
	return False #TODO gérer le cas où le fichier n'est pas trouvé
