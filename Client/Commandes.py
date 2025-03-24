import EnvoiClient 
import Header

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
			
def commandeGet(client_socket, conf, fichier):
	message = Header. CreateGetHeader(fichier)
	if EnvoiClient.canSend():
		client_socket.sendto(message.encode(), conf["AdresseServeur"])
		i = 0
		receivedData = []
		messageConfirmation = "RECEIVED"
		while True:
			client_socket.settimeout(3)
			data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))
			if data:
				i += 1
				receivedData.append(data)
			if i == 4 or True in data.decode():
				client_socket.sendto(messageConfirmation.encode(), conf["AdresseServeur"])
				i = 0
		##Fichier dans telechargement 
		##reception du message
		##decodage
		##verification du fichier
		##verification de la somme
		##assemblage et affichage de la barre de telechargement 
		##reception de la fin
		##envoie des confirmation
		##Indiquer que le telechargement est complet
		
def commandeLs(client_socket, conf):
	str = Header.CreateLsHeader()
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode().strip()
		print("Fichier disponibles : ")
		print(message) 
		

			