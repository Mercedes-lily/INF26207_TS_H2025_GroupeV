#Fonctions pour batir les différent header

#Fonction pour le header du 3-way
def CreateThreeWayHeader(message, conf) :
	message += "Taille:"+ conf["DataSize"].strip() + "\r\n"
	message += "NombreMorceaux:" + conf["DataConfirmation"].strip() + "\r\n"
	message += "TailleHeader:100\r\n"
	while(len(message) != 100):
		message += " "
	return message

#Fonction pour le header de la fonction get
def CreateGetHeaderServeur(fichier, islast, donnee, numero):
	message += "Fichier:" + fichier + "\r\n"
	message += "Dernier:" + islast + "\r\n"
	message += "NumeroMorceaux:" + numero + "\r\n"
	message += "Checksum:"+ len(donnee) + "\r\n"
	message += "TailleHeader:100\r\n"
	while(len(message) != 100):
		message += " "
	message + donnee
	return message

#Fonction pour le header de la fonction by
def CreateByeHeaderServeur():
	message = "bye\r\n"
	while(len(message) != 100):
		message += " "
	return message

#Fonction pour le header de la fonction ls
def CreateLsHeaderServeur(files):
	message = ""
	if not files:
		message += "Aucun fichier disponible."
	else:
		for file in files:
			message += file + "\r\n"
	return message