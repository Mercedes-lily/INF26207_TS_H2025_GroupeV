#Fonction liés aux sockets
import socket

adresse = "127.0.0.1"
port = 2212
serveur_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serveur_socket.bind(adresse, port)
    

# try:
#   print(x)
# except:
#   print("An exception occurred")
