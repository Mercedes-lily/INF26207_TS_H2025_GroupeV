import EnvoiClient 
import Header
import os
import socket

DOWNLOAD_DIR = "Client\Telechargements"

def AideCommandes():
	print("Veuillez entrer une commande parmi :")
	print("		ls : Pour connaitre les fichier téléchargables")
	print("		get NomDuFichier: Pour télécharger le fichier demandé")
	print("		bye : pour vous reconnecter")

def commandeBye(client_socket, conf):    ##comment pour la boucle de renvoie
	str = Header.CreateByeHeader()
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode().strip()
		if(message == "bye\r\n"):
			print("Déconnection effectué")



# # Configuration du client
# SERVER_HOST = '127.0.0.1'  # Adresse IP du serveur (localhost par défaut)
# SERVER_PORT = 2212         # Port du serveur
# BUFFER_SIZE = 1024         # Taille du buffer pour recevoir les données
# DOWNLOAD_DIR = "telechargements"  # Dossier pour stocker les fichiers téléchargés

# # Création du socket UDP
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.settimeout(3)  # Timeout de 3 secondes pour les réponses

# # Fonction pour envoyer une commande au serveur
# def send_command(command):
#     """
#     Envoie une commande au serveur et attend la réponse.

#     :param command: La commande à envoyer (par exemple, "get fichier.txt").
#     """
#     client_socket.sendto(command.encode(), (SERVER_HOST, SERVER_PORT))
#     print(f"Commande envoyée au serveur : {command}")

# # Fonction pour recevoir un fichier du serveur
# def receive_file(filename):
#     """
#     Reçoit un fichier du serveur en morceaux et le réassemble.

#     :param filename: Le nom du fichier à télécharger.
#     """
#     # Créer le dossier de téléchargement s'il n'existe pas
#     if not os.path.exists(DOWNLOAD_DIR):
#         os.makedirs(DOWNLOAD_DIR)

#     file_path = os.path.join(DOWNLOAD_DIR, filename)
#     received_chunks = {}  # Dictionnaire pour stocker les morceaux reçus
#     expected_chunk_number = 0  # Numéro du morceau attendu

#     print(f"Téléchargement du fichier {filename}...")

#     while True:
#         try:
#             # Recevoir un morceau du serveur
#             data, server_address = client_socket.recvfrom(BUFFER_SIZE + 50)  # +50 pour l'en-tête
#             header = data.decode().split(":")  # Décoder l'en-tête
#             chunk_number = int(header[1])  # Numéro du morceau
#             chunk_data = data.split(b":", 2)[2]  # Données du morceau

#             # Vérifier si c'est la fin du fichier
#             if header[0] == "EOF":
#                 print("Téléchargement terminé.")
#                 break

#             # Stocker le morceau reçu
#             received_chunks[chunk_number] = chunk_data

#             # Envoyer un accusé de réception au serveur
#             ack_message = f"ACK:{chunk_number}"
#             client_socket.sendto(ack_message.encode(), server_address)
#             print(f"Accusé de réception envoyé pour le morceau {chunk_number}")

#             # Réassembler les morceaux dans l'ordre
#             if chunk_number == expected_chunk_number:
#                 with open(file_path, "ab") as file:  # Mode "append binary"
#                     while expected_chunk_number in received_chunks:
#                         file.write(received_chunks[expected_chunk_number])
#                         del received_chunks[expected_chunk_number]
#                         expected_chunk_number += 1

#         except socket.timeout:
#             print("Timeout : Aucun morceau reçu. Attente du prochain...")
#             continue

#     print(f"Fichier enregistré dans {file_path}")

# # Fonction pour gérer la commande "get"
# def get_command(filename):
#     """
#     Envoie une commande "get" au serveur et reçoit le fichier.

#     :param filename: Le nom du fichier à télécharger.
#     """
#     send_command(f"get\r\n{filename}")  # Envoyer la commande "get"
#     receive_file(filename)  # Recevoir le fichier

# # Boucle d'écoute pour interagir avec l'utilisateur
# def main_loop():
#     while True:
#         print("\nCommandes disponibles :")
#         print("1. get <nom_fichier> - Télécharger un fichier")
#         print("2. exit - Quitter le programme")
#         user_input = input("Entrez une commande : ").strip()

#         if user_input.startswith("get"):
#             filename = user_input.split()[1]
#             get_command(filename)
#         elif user_input == "exit":
#             print("Déconnexion...")
#             break
#         else:
#             print("Commande invalide. Veuillez réessayer.")

# # Exécution du programme
# if __name__ == "__main__":
#     main_loop()
#     client_socket.close()

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


def commandeGet(client_socket, conf, fichier):
	str = Header.CreateGetHeader(fichier)
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		receive_file(client_socket, conf, fichier)
		
def commandeLs(client_socket, conf):
	str = Header.CreateLsHeader()
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode().strip()
		print("Fichier disponibles : ")
		print(message) 
		

			