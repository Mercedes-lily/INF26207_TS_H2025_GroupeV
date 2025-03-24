#Fichiers de bases du coté Client
#Librairie pour utiliser les sockets

import Commandes
import Utilitaires
import threeWayHandShake
import socket

def receiveFile(client_socket, conf):
	i = 0
	while i < 10:
		data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))
		message = data.decode()
		print("Message reçu : " + message)
		i+=1

def loop_client(client_socket, conf):
	isconnect = True
	Commandes.AideCommandes()
	while(isconnect == True):
		str = input(":>")
		if not str:
			continue
		strSplit = str.split()
		if(str.strip() == "ls"):
			Commandes.commandeLs(client_socket, conf)
		elif(strSplit[0].strip() == "ls"and len(strSplit) != 1):
			print("Veuillez entrer la commande ls uniquement")
		elif (str.strip() == "bye"):
			Commandes.commandeBye(client_socket, conf)
			isconnect = False
		elif(strSplit[0].strip() == "bye"and len(strSplit) != 1):
			print("Veuillez entrer la commande bye uniquement")
		elif(strSplit[0].strip() == "get"and len(strSplit) == 2):
			Commandes.commandeGet(client_socket, conf, strSplit[1])
			receiveFile(client_socket, conf)
		elif(strSplit[0].strip() == "get"and len(strSplit) != 2):
			print("La commande get doit  être écrite comme suit : get NomDuFichier.Extention")
		elif(strSplit[0].strip() == "open"):
			print("Veuillez fermer la connection avec le serveur en cours avec la commande bye avant de vous connecter à un nouveau serveur")
		else:
			Commandes.AideCommandes()

#Initialisation du côté client et implémentation du three-Way Handshake
def SocketStart(conf, isconnect, addr):
	serv_adresse = (addr, 2212)  #changer pour celui que on va recevoir de lentree du client
	conf["AdresseServeur"] = serv_adresse
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while (isconnect == False):
		isconnect = threeWayHandShake.ThreeWay(conf, client_socket, serv_adresse)
	return client_socket


def OuvertureClient():
	print("Bienvenue !")
	while True:
		str = input("Veuillez entrer open et l'adresse IPv4 du serveur auquel vous voulez vous connecter :>")
		if not str:
			continue
		strSplit = str.split()
		if(len(strSplit) == 2 and  strSplit[0] == "open"):
			return strSplit[1]
		elif(len(strSplit) > 2 and  strSplit[0] == "open"):
			print("Entrée invalide : Une seule adresse IPv4 est permise")
		elif(len(strSplit) < 2 and  strSplit[0] == "open"):
			print("Entrée invalide : Une adresse doit être entré")
		else:
			print("Entrée invalide : Vous devez d'abord vous connecter avec la commande open")

def main():
    addr = OuvertureClient()
    isconnect = False
    conf = Utilitaires.lectureConfigurationFile()
    client_socket = SocketStart(conf, isconnect, addr)
    loop_client(client_socket, conf)

if __name__ == "__main__":
	main()


# ls  --->    ls\r\n    get test.txt---->    get\r\ntest.txt\r\n