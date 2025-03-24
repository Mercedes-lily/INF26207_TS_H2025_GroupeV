import EnvoiClient 
import Header
import os
import socket

DOWNLOAD_DIR = "Client\Telechargements"

#Fonction qui explique les commandes permises
def AideCommandes():
	print("Veuillez entrer une commande parmi :")
	print("		ls : Pour connaitre les fichier téléchargables")
	print("		get NomDuFichier: Pour télécharger le fichier demandé")
	print("		bye : pour vous reconnecter")

#Fonction qui execute la commande bye 
def commandeBye(client_socket, conf):    ##comment pour la boucle de renvoie
	str = Header.CreateByeHeader()
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode().strip()
		if(message == "bye\r\n"):
			print("Déconnection effectué")


# Fonction pour recevoir un fichier du serveur
def receive_file(client_socket, conf, filename):
	"""
	Reçoit un fichier du serveur en morceaux et le réassemble.

    :param filename: Le nom du fichier à télécharger.
    """
	client_socket.settimeout(3)
    # Créer le dossier de téléchargement s'il n'existe pas
	if not os.path.exists(DOWNLOAD_DIR):
		os.makedirs(DOWNLOAD_DIR)

	file_path = os.path.join(DOWNLOAD_DIR, filename)
	print(file_path)
	received_chunks = {}  # Dictionnaire pour stocker les morceaux reçus
	expected_chunk_number = 0  # Numéro du morceau attendu
	BlocConfirmation = int(conf["DataConfirmation"])

	print(f"Téléchargement du fichier {filename}...")
	while True:
		try:
            # Recevoir un morceau du serveur
			data, server_address = client_socket.recvfrom(int(conf["DataSize"]))
			encodeHeader = data[:100]
			decodeHeader = encodeHeader.decode()
			decodeHeaderSplit = decodeHeader.split("\r\n")
			header = {}
			for i in range(0, 5):
				dataInfo = decodeHeaderSplit[i].strip().split(":")
				header[dataInfo[0]] = dataInfo[1]
			chunk_data = data[100:]
			print(chunk_data)
			chunk_number = int(header["NumeroMorceaux"])  # Numéro du morceau

            # Stocker le morceau reçu
			received_chunks[chunk_number] = chunk_data

            # Envoyer un accusé de réception au serveur
			if((chunk_number % BlocConfirmation == BlocConfirmation - 1) or header["Dernier"] == "True"):
				ConfirmationHeader = Header.CreateConfirmationHeader(chunk_number)
				client_socket.sendto(ConfirmationHeader.encode(), server_address)
				print(f"Accusé de réception envoyé pour le morceau {chunk_number}")

            # Réassembler les morceaux dans l'ordre
			if chunk_number == expected_chunk_number:
				with open(file_path, "ab") as file:
					while expected_chunk_number in received_chunks:
						file.write(received_chunks[expected_chunk_number])
						del received_chunks[expected_chunk_number]
						expected_chunk_number += 1
				            # Vérifier si c'est la fin du fichier
			if header["Dernier"] == "True":
				print("Téléchargement terminé.")
				return
		except socket.timeout:
			print("Timeout : Aucun morceau reçu. Attente du prochain...")
			continue
	print(f"Fichier enregistré dans {file_path}")


#Fonction qui execute la commande get
def commandeGet(client_socket, conf, fichier):
	str = Header.CreateGetHeader(fichier)
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		receive_file(client_socket, conf, fichier)
		
#Fonction qui execute la fonction ls
def commandeLs(client_socket, conf):
	str = Header.CreateLsHeader()
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode().strip()
		print("Fichier disponibles : ")
		print(message) 
		

			