#Fonctions pour batir les différent header

#Fonction pour le header du 3-way
def CreateThreeWayHeader(message, conf) :
	message += "Taille:"+ conf["DataSize"].strip() + "\r\n"
	message += "NombreMorceaux:" + conf["DataConfirmation"].strip() + "\r\n"
	tailleheader = len(message) + len("TailleHeader:") + 4
	tailleheader += len(str(tailleheader))
	message += "TailleHeader:" + str(tailleheader) + "\r\n"
	message += "\r\n"
	return message

#Fonction pour le header de la fonction get
def CreateGetHeaderServeur(conf, fichier, islast, donnee, numero):
	message = islast + "\r\n"
	message += "Fichier:" + fichier + "\r\n"
	message += "NumeroMorceaux:" + numero + "\r\n"
	message += "Checksum:"+ len(donnee) + "\r\n"
	tailleheader = len(message) + len("TailleHeader:") + len("Donnees:") + len(donnee) + len ("\r\n") 
	tailleheader += len(str(tailleheader)) + 4
	message += "TailleHeader:" + str(tailleheader) + "\r\n"
	message +="Donnees:" + donnee + "\r\n"
	message += "\r\n"
	return message

#Fonction pour le header de la fonction get
def CreateByeHeaderServeur(conf, fichier, islast, donnee, numero):
	return 0
	#Fonction pour le header de la fonction get

def CreateLsHeaderServeur(conf, fichier, islast, donnee, numero):
		return 0