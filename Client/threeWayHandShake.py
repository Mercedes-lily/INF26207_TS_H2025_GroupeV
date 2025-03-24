# Fonction liés à la reception du serveur
import Header
import socket
import EnvoiClient

#Fonction qui permet de négicier la taille de la fenêtre, mais aussi 
# le nombre de morceaux à envoyer avant la confirmation par le client
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

#Fonction qui gère la poignée de main 
def ThreeWay(conf, client_socket, serv_adresse):     ##Prob. ici
	message = Header.CreateThreeWayHeader("SYN\r\n", conf)
	if EnvoiClient.canSend():
		client_socket.sendto(message.encode(), serv_adresse)
	client_socket.settimeout(10)
	data, serv_adresse = client_socket.recvfrom(int(conf["DataSize"]))  #Recoit jusqua datasize byte
	message = data.decode()
	print(f"Received data from {serv_adresse}: {message}") 
	if negociation(message, conf) == True:
		message = Header.CreateThreeWayHeader("ACK\r\n", conf)
		if EnvoiClient.canSend():
			client_socket.sendto(message.encode(), serv_adresse)
			return True
		else:
			print("Erreur envoie")
	return False