#Fichiers de bases du coté Serveur
#Librairie pour utiliser les sockets
import socket   

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
    

#Initialisation du socket UDP du côté serveur et implémentation du three-Way Handshake
#Lecture necessaire dna sun fichier de configuration
def ServeurStart(conf):
    port = 2212
    adresse = "127.0.0.1"
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        serv_socket.bind((adresse, port))
        print("Bind : Succes")
    except Exception as e:
        print("Bind : Echec, error: " + e)
        exit()
    serv_socket.settimeout(7)
    data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
    data_decode = data.decode()
    print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
    if data_decode == "SYN":
        serv_socket.settimeout(5)
        message = "SYN-ACK"  
        serv_socket.sendto(message.encode(), client_adresse)
    data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
    print(f"Received data from {client_adresse}: {data.decode()}") #decodes the recieved bytes.
    if data.decode() == "ACK":
        print("3 way : reussi")

    return serv_socket
    

def main():
    print("L'adresse ipv4 de ce serveur est : 127.0.0.1")
    conf = lectureConfigurationFile()
    serv_socket = ServeurStart(conf)


    

if __name__ == "__main__":
    main()
