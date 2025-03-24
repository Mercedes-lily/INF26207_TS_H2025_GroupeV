#Fonction de découpage de l'information afin de l'utilisé

#Fonction pour le header de la fonction bye
def CreateByeHeader():
	message = "bye\r\n"
	while(len(message) != 100):
		message += " "
	return message

#Fonction pour le header de la fonction ls
def CreateLsHeader():
	message = "ls\r\n"
	while(len(message) != 100):
		message += " "
	return message

#Fonction pour le header de la fonction get
def CreateGetHeader(fichier):
	message = "get" + fichier +"\r\n"
	message += "TailleHeader:100\r\n"
	while(len(message) != 100):
		message += " "
	return message

#Fonction pour le header pour l'envoi d'une confirmation
def CreateConfirmationHeader(last):
	message += "Confirmation\r\n"
	message += "DernierMorceaux:" + last + "\r\n"
	message += "TailleHeader:100" + "\r\n"
	while(len(message) != 100):
		message += " "
	return message

#Fonction pour le header pour de la poignée de main
def CreateThreeWayHeader(message, conf) :
	message += "Taille:"+ conf["DataSize"].strip() + "\r\n"
	message += "NombreMorceaux:" + conf["DataConfirmation"].strip() + "\r\n"
	message += "TailleHeader:100\r\n"
	while(len(message) != 100):
		message += " "
	return message