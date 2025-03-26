import EnvoiClient 
import Header
import os
import socket

#Endroit où enregistrer les fichiers téléchargés
DOWNLOAD_DIR = "Client\Telechargements"

#Fonction qui explique les commandes permises
def AideCommandes():
	print("Veuillez entrer une commande parmi :")
	print("		ls : Pour connaitre les fichier téléchargables")
	print("		get NomDuFichier: Pour télécharger le fichier demandé")
	print("		bye : pour vous reconnecter")

#Fonction qui execute la commande bye 
def commandeBye(client_socket, conf):
	str = Header.CreateByeHeader()
	if EnvoiClient.canSend(float(conf["Fiabilite"])):
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))
		message = data.decode().strip()
		if(message == "bye\r\n"):
			print("Déconnection effectué")


# Fonction pour recevoir un fichier du serveur
# Reçoit un fichier du serveur en morceaux et le réassemble.
def receive_file(client_socket, conf, filename):
    # Créer le dossier de téléchargement s'il n'existe pas
	if not os.path.exists(DOWNLOAD_DIR):
		os.makedirs(DOWNLOAD_DIR)

	#Concatene le dossier avec le fichier è transférer
	file_path = os.path.join(DOWNLOAD_DIR, filename)
	received_chunks = {}  # Dictionnaire pour stocker les morceaux reçus
	expected_chunk_number = 0  # Numéro du morceau attendu
	BlocConfirmation = int(conf["DataConfirmation"])

	print(f"Téléchargement du fichier {filename}...")
	while True:
		try:
            # Recevoir un morceau du serveur
			data, server_address = client_socket.recvfrom(int(conf["DataSize"]))
			encodeHeader = data[:100] #On sort les données du header qui sont de taille 100
			decodeHeader = encodeHeader.decode() #C'est données on été encodé en binaire et on doit les decoder avant de les lire
			decodeHeaderSplit = decodeHeader.split("\r\n")
			header = {}
			for i in range(0, 5):
				dataInfo = decodeHeaderSplit[i].strip().split(":")
				header[dataInfo[0]] = dataInfo[1]
			chunk_data = data[100:] #Ce sont les données brutes du document
			chunk_number = int(header["NumeroMorceaux"])  # Numéro du morceau

            # Stocker le morceau reçu
			received_chunks[chunk_number] = chunk_data

            # Envoyer un accusé de réception au serveur si on arrive au bon nombre de morceau ou à la fin du fichier
			if((chunk_number % BlocConfirmation == BlocConfirmation - 1) or header["Dernier"] == "True"):
				ConfirmationHeader = Header.CreateConfirmationHeader(chunk_number)
				if EnvoiClient.canSend(float(conf["Fiabilite"])):
					client_socket.sendto(ConfirmationHeader.encode(), server_address)
					print(f"Accusé de réception envoyé pour le morceau {chunk_number}")

            # Réassembler les morceaux dans l'ordre. Si c'est le premier morceau et qu'il y a un fichier du même nom, le remplacer
			if chunk_number == expected_chunk_number:
				if chunk_number == 0:
					with open(file_path, "wb") as file:
						file.write(received_chunks[expected_chunk_number])
						file.close()
						del received_chunks[expected_chunk_number]
						expected_chunk_number += 1
				with open(file_path, "ab") as file: 
					while expected_chunk_number in received_chunks:
						file.write(received_chunks[expected_chunk_number])
						del received_chunks[expected_chunk_number]
						expected_chunk_number += 1
			# Vérifier si c'est la fin du fichier
			if header["Dernier"] == "True":
				print("Téléchargement terminé.")
				return
		except socket.timeout: #Attente lorsque le délai est trop long avant de recevoir les données du serveur
			print("Timeout : Aucun morceau reçu. Attente du prochain...")
			continue


#Fonction qui execute la commande get
def commandeGet(client_socket, conf, fichier):
	str = Header.CreateGetHeader(fichier)
	if EnvoiClient.canSend(float(conf["Fiabilite"])):
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		receive_file(client_socket, conf, fichier)
		
#Fonction qui execute la fonction ls
def commandeLs(client_socket, conf):
	str = Header.CreateLsHeader()
	if EnvoiClient.canSend(float(conf["Fiabilite"])):
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))
		message = data.decode().strip()
		print("Fichier disponibles : ")
		print(message) 
		

			