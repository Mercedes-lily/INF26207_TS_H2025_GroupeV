#Fonction liés aux sockets

import socket
import Envoie

def threeWay(conf, serv_socket):
    try:
        serv_socket.settimeout(0.1)
        tried = 0
        while True:
            try:
                data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
                if not data:
                    break  # Connexion fermée par l'hôte distant
                data_decode = data.decode()
                print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
                if data_decode == "SYN" or (tried <= 5 and data_decode != "ACK"):
                    serv_socket.settimeout(3)
                    message = "SYN-ACK"
                    if Envoie.canSend():
                        tried += 1
                        serv_socket.sendto(message.encode(), client_adresse)
                elif data.decode() == "ACK":
                    print("3 way : reussi")
                    return serv_socket
            except socket.timeout:
                pass  # Ignorer les délais d'attente et continuer
    except KeyboardInterrupt:
        print("3 way : Echec (Ctrl+C)")
    
# data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
#         data_decode = data.decode()
#         print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
#         if data_decode == "SYN":
#             serv_socket.settimeout(5)
#             message = "SYN-ACK"
#             if Envoie.canSend():
#                 serv_socket.sendto(message.encode(), client_adresse)
#         data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
#         print(f"Received data from {client_adresse}: {data.decode()}") #decodes the recieved bytes.
#         if data.decode() == "ACK":
#             print("3 way : reussi")
#         return serv_socket
    

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
    # serv_socket.settimeout(7)
    return threeWay(conf, serv_socket)