#Fonction liés aux sockets
import socket
import EnvoiClient

def commandeBye(client_socket, conf):    ##comment pour la boucle de renvoie
	str = "bye\r\n"
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode()
		if(message == "bye\r\n"):
			print("Déconnection effectué")

def CreateGetHeader(fichier):
	message += "get" + fichier +"\r\n"
	tailleheader = len(message) + len("TailleHeader:")
	tailleheader += len(str(tailleheader)) + 4
	message += "TailleHeader:" + str(tailleheader) + "\r\n"
	message += "\r\n"
	return message

def CreateConfirmationHeader(last):
	message += "Confirmation:" + "\r\n"
	message += "DernierMorceaux:" + last + "\r\n"
	tailleheader = len(message) + len("TailleHeader:")
	tailleheader += len(str(tailleheader)) + 4
	message += "TailleHeader:" + str(tailleheader) + "\r\n"
	message += "\r\n"
	return message


def commandeGet(client_socket, conf, fichier):
	str = "get\r\n"
	str += fichier + "\r\n"
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
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
	str = "ls\r\n"
	if EnvoiClient.canSend():
		client_socket.sendto(str.encode(), conf["AdresseServeur"])
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
		message = data.decode()
		print(message) 

def AideCommandes():
	print("Veuillez entrer une commande parmi :")
	print("		ls : Pour connaitre les fichier téléchargables")
	print("		get NomDuFichier: Pour télécharger le fichier demandé")
	print("		bye : pour vous reconnecter")
    

def loop_client(client_socket, conf):
	isconnect = True
	AideCommandes()
	while(isconnect == True):
		str = input(":>")
		strSplit = str.split()
		if(str.strip() == "ls"):
			commandeLs(client_socket, conf)
		elif(strSplit[0].strip() == "ls"and len(strSplit) != 1):
			print("Veuillez entrer la commande ls uniquement")
		elif (str.strip() == "bye"):
			commandeBye(client_socket, conf)
			isconnect = False
		elif(strSplit[0].strip() == "bye"and len(strSplit) != 1):
			print("Veuillez entrer la commande bye uniquement")
		elif(strSplit[0].strip() == "get"and len(strSplit) == 2):
			commandeGet(client_socket, conf, strSplit[1])
		elif(strSplit[0].strip() == "get"and len(strSplit) != 2):
			print("La commande get doit  être écrite comme suit : get NomDuFichier.Extention")
		elif(strSplit[0].strip() == "open"):
			print("Veuillez fermer la connection avec le serveur en cours avec la commande bye avant de vous connecter à un nouveau serveur")
		else:
			AideCommandes()


def negociation(message, conf):
	splitmessage = message.split("\r\n")
	if(splitmessage[0] != "SYN-ACK"):
		print("SYN-ACK erreur")
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
	if(conf["DataSize"] > dataRecu["Taille"]):
		conf["DataSize"] = dataRecu["Taille"]
	if(conf["DataConfirmation"] > dataRecu["NombreMorceaux"]):
		conf["DataConfirmation"] = dataRecu["NombreMorceaux"]
	return True

def CreateThreeWayHeader(message, conf) :
	message += "Taille:"+ conf["DataSize"].strip() + "\r\n"
	message += "NombreMorceaux:" + conf["DataConfirmation"].strip() + "\r\n"
	tailleheader = len(message) + len("TailleHeader:") 
	tailleheader += len(str(tailleheader)) + 4
	message += "TailleHeader:" + str(tailleheader) + "\r\n"
	message += "\r\n"
	return message

def ThreeWay(conf, client_socket, serv_adresse):     ##Prob. ici
	message = CreateThreeWayHeader("SYN\r\n", conf)
	if EnvoiClient.canSend():
		client_socket.sendto(message.encode(), serv_adresse)
	client_socket.settimeout(3)
	data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
	message = data.decode()
	print(f"Received data from {serv_adresse}: {message}") 
	if negociation(message, conf) == True:
		message = CreateThreeWayHeader("ACK\r\n", conf)
		if EnvoiClient.canSend():
			client_socket.sendto(message.encode(), serv_adresse)
			return True
		else:
			print("Erreur envoie")
	return False

#Initialisation du côté client et implémentation du three-Way Handshake
def SocketStart(conf, isconnect, addr):
	serv_adresse = (addr, 2212)  #changer pour celui que on va recevoir de lentree du client
	conf["AdresseServeur"] = serv_adresse
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while (isconnect == False):
		isconnect = ThreeWay(conf, client_socket, serv_adresse)
	return client_socket


