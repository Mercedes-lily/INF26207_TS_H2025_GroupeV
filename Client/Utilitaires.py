#Fonctions utiles en générales

def Validite(conf):
    if("Timeout" not in conf):
        conf["Timeout"] = "3"
    if("DataSize" not in conf):
        conf["DataSize"] = "25000"
    if("DataConfirmation" not in conf):
        conf["DataConfirmation"] = "5"

def lectureConfigurationFile():
    dictionnaireConfiguration = {}
    with open("Client/Client.conf", 'r') as fichier:
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