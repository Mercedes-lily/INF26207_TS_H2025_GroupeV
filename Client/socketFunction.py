#Fonction liés aux sockets
import socket
import EnvoiClient

#Envoie open (Syn)
#Commande\r\nadresse ip\r\nTaille du Header\r\nTaille proposé\r\nNombre de morceaux maximales avant l'accusé de réception proposé\r\n\r\n
#Syn\r\n127.0.0.0\r\nTailleHeader:37\r\nTaille:30000\r\nNombreMorceaux:3\r\n\r\n

def commandeBye():
	return 0

def commandeGet():
	return 0

def commandeLs():
	return 0

def loop_client(isconnect):
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

def ThreeWay(conf, client_socket, serv_adresse):
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
	conf["IP"] = addr
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while (isconnect == False):
		isconnect = ThreeWay(conf, client_socket, serv_adresse)
	return client_socket
