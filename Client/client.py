#Fichiers de bases du coté Client
#Librairie pour utiliser les sockets
import socket   

#Initialisation du côté client et implémentation du three-Way Handshake
def SocketStart():
    serveur_port = 2212
    serveur_adresse = "127.0.0.1"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "SYN"
    client_socket.sendto(message.encode(), (serveur_adresse, serveur_port))
    client_socket.settimeout(5)
    data, serv_adresse = client_socket.recvfrom(1024)  # Receive up to 1024 bytes
    print(f"Received data from {serv_adresse}: {data.decode()}") #decodes the recieved bytes.
    if data.decode() == "SYN-ACK":
        message = "ACK"  
        client_socket.sendto(message.encode(), serv_adresse)

def main():
    SocketStart()
    

if __name__ == "__main__":
    main()