#Fonction liés à la poignée de main
import Commandes
import EnvoiServeur
import Header
import socket

#Négociation des tailles de la taille de la fenêtre et du nombre de morceau avant la confirmation
def negociation(message, conf, SYNACK):
	splitmessage = message.split("\r\n")
	if(splitmessage[0] != SYNACK):
		return False #pas le bon syn ou ack
	dataRecu = {}
	for m in splitmessage:
		splitm = m.split(":")
		if len(splitm) == 1:
			continue
		dataRecu[splitm[0]] =  splitm[1]
	if(int(dataRecu["TailleHeader"]) != len(message)):
		print("difference de taille")
		print("    ")
		return False
	if(conf["DataSize"] != dataRecu["Taille"]):
		conf["DataSize"] = dataRecu["Taille"]
	if(conf["DataConfirmation"] > dataRecu["NombreMorceaux"]):
		conf["DataConfirmation"] = dataRecu["NombreMorceaux"]
	print("nego done")
	return True

#Fonction principale du 3-way
def threeWay(conf, serv_socket):
	try:
		serv_socket.settimeout(0.1)
		tried = 0
		while True:
			try:
				data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
				if not data or tried > 4:
					break  #TODO Connexion fermée par l'hôte distant ############UTILE? 
				message = data.decode()
				print(f"Received data from {client_adresse}: {message}")
				if negociation(message, conf, "SYN") == True:
					print("tried: " + str(tried))
					print("negociation")
					serv_socket.settimeout(3)
					message = Header.CreateThreeWayHeader("SYN-ACK\r\n", conf)
					tried += 1
					if EnvoiServeur.canSend():
						serv_socket.sendto(message.encode(), client_adresse)
					else:
						print("Erreur envoie")
				elif negociation(message, conf, "ACK") == True:
					data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
					print(f"Received data from {client_adresse}: {data.decode()}")
					if(data.decode().strip(" \r\n") == "ls"):
						Commandes.handle_ls_command(client_adresse, serv_socket)
					if(data.decode().strip(" \r\n") == "bye"):
						Commandes.handle_bye_command(client_adresse, serv_socket)
			except socket.timeout:
				pass  # Ignorer les délais d'attente et continuer
	except KeyboardInterrupt:
		print("3 way : Echec (Ctrl+C)")
