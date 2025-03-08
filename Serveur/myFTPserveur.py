#Fichiers de bases du coté Serveur
#Librairie pour utiliser les sockets
import socket   


#Initialisation du socket UDP du côté serveur et implémentation du three-Way Handshake
def ServeurStart():
    port = 2212
    adresse = "127.0.0.1"
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        serv_socket.bind((adresse, port))
        print("Bind : Succes")
    except Exception as e:
        print("Bind : Echec, error: " + e)
        exit()
    serv_socket.settimeout(5)
    data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
    data_decode = data.decode()
    print(f"Received data from {client_adresse}: {data_decode}") #decodes the recieved bytes.
    print(data_decode == "SYN")
    print("--" + data_decode + "--")
    if data_decode == "SYN":
        message = "SYN-ACK"  
        serv_socket.sendto(message.encode(), client_adresse)
    data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
    print(f"Received data from {client_adresse}: {data.decode()}") #decodes the recieved bytes.
    if data.decode() == "ACK":
        print("3 way : reussi")
    
    return serv_socket
    

def main():
    print("L'adresse ipv4 de se serveur est : 127.0.0.1")
    serv_socket = ServeurStart()


    

if __name__ == "__main__":
    main()
