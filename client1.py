#%%
import socket

# socket hôte A
sock_A = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # mode UDP

# on lie le socket A à une adresse du réseau de rebouclage et un port whatever
sock_A.bind(("127.0.0.1", 5653))

# tant qu'on veut que la connexion soit "maintenue"
while True:
    data, address = sock_A.recvfrom(4096) # on reçoit des données, et les coordonées de l'expéditeur

    if data: # on vérifie qu'on a des données
        data = data.decode(encoding='utf-8') # dans ce cas ci je reçois du texte en utf-8
        print(f"reçu {data} de {address}")

        if data == "quit": # si je reçois un message de terminaison...
            sock_A.shutdown(socket.SHUT_RDWR) # pas vraiment nécessaire pour UDP, mais, whatever
            sock_A.close() # on ferme le socket
            break # adios amigos