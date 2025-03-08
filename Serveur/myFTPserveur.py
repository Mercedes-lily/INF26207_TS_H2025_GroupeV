#Fichiers de bases du coté Serveur
import socket   

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

    try:
        data, client_adresse = serv_socket.recvfrom(1024)  # Receive up to 1024 bytes
        print(f"Received data from {client_adresse}: {data.decode()}") #decodes the recieved bytes.
        print("Receive : Succes")

    except Exception as e:
        print(f"Receive : Echec, error: {e}")
        exit()
    

def main():
    ServeurStart()
    

if __name__ == "__main__":
    main()
