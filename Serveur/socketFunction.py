#Fonction liés aux sockets

import socket
import Envoie

def negociation(message, conf, SYNACK):   # regarder le SYN
    splitmessage = message.split("\r\n")
    if(splitmessage[0] != SYNACK):
        print("pas le bon syn ou ack")
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
    if(conf["DataSize"] != dataRecu["Taille"]):
        conf["DataSize"] = dataRecu["Taille"]
    if(conf["DataConfirmation"] > dataRecu["NombreMorceaux"]):
        conf["DataConfirmation"] = dataRecu["NombreMorceaux"]
    return True

def CreateThreeWayHeader(message, conf) :
    message += "Taille:"+ conf["DataSize"].strip() + "\r\n"
    message += "NombreMorceaux:" + conf["DataConfirmation"].strip() + "\r\n"
    tailleheader = len(message) + len("TailleHeader:") + 4
    tailleheader += len(str(tailleheader))
    message += "TailleHeader:" + str(tailleheader) + "\r\n"
    message += "\r\n"
    return message

#reste le temps dattente et aussi le retourner si le ack nest pas satisfait
def threeWay(conf, serv_socket):
    data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
    message = data.decode()
    print(f"Received data from {client_adresse}: {message}")
    if negociation(message, conf, "SYN") == True:
        print("negociation")
        serv_socket.settimeout(5)
        message = CreateThreeWayHeader("SYN-ACK\r\n", conf)
        serv_socket.sendto(message.encode(), client_adresse)
    data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
    message = data.decode()
    print(f"Received data from {client_adresse}: {data.decode()}")
    if negociation(message, conf, "ACK") == True:
        print("3 way : reussi")

# try:
#         serv_socket.settimeout(0.1)
#         tried = 0
#         while True:
#             try:
#                 data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
#                 if not data:
#                     break  # Connexion fermée par l'hôte distant
#                 data_decode = data.decode()
#                 print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
#                 if data_decode == "SYN" or (tried <= 5 and data_decode != "ACK"):
#                     serv_socket.settimeout(3)
#                     message = "SYN-ACK"
#                     if Envoie.canSend():
#                         tried += 1
#                         serv_socket.sendto(message.encode(), client_adresse)
#                 elif data.decode() == "ACK":
#                     print("3 way : reussi")
#                     return serv_socket
#             except socket.timeout:
#                 pass  # Ignorer les délais d'attente et continuer
#     except KeyboardInterrupt:
#         print("3 way : Echec (Ctrl+C)")
    
# # data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
# #         data_decode = data.decode()
# #         print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
# #         if data_decode == "SYN":
# #             serv_socket.settimeout(5)
# #             message = "SYN-ACK"
# #             if Envoie.canSend():
# #                 serv_socket.sendto(message.encode(), client_adresse)
# #         data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
# #         print(f"Received data from {client_adresse}: {data.decode()}") #decodes the recieved bytes.
# #         if data.decode() == "ACK":
# #             print("3 way : reussi")
#         # return serv_socket
#Initialisation du socket UDP du côté serveur et implémentation du three-Way Handshake
#Lecture necessaire dna sun fichier de configuration
def ServeurStart(conf):
    port = 2212
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        serv_socket.bind((conf["IPv4"], port))
        print("Bind : Succes")
    except Exception as e:
        print("Bind : Echec, error: " + e)
        exit()
    serv_socket.settimeout(10)
    threeWay(conf, serv_socket)
    return serv_socket 

