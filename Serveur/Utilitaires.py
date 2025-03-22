#Fonctions utiles en générales

#Fonctions qui permet de vérifier si toutes les informations sont dans le fichier de configuration
def Validite(conf):
	if("Port" not in conf):
		conf["Port"] = "2212"
	if("IPv4" not in conf):
		conf["IPv4"] = "127.0.0.1"
	if("Timeout" not in conf):
		conf["Timeout"] = "3"
	if("DataSize" not in conf):
		conf["DataSize"] = "25000"
	if("DataConfirmation" not in conf):
		conf["DataConfirmation"] = "6"
	if("Encode" not in conf):
		conf["Encode"] = "UTF-8"

#Fonctions qui permet de lire le fichier de configuration
def lectureConfigurationFile():
	dictionnaireConfiguration = {}
	with open("Serveur/Serveur.conf", 'r') as fichier:
		line = fichier.readline()
		while line:
			splitline = line.split(":")
			if(len(splitline) == 1):
				line = fichier.readline()
				continue
			dictionnaireConfiguration[splitline[0]] = splitline[1].strip("\n")
			line = fichier.readline()
		print(dictionnaireConfiguration)
		Validite(dictionnaireConfiguration)
		print(dictionnaireConfiguration)
	return dictionnaireConfiguration