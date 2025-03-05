import socket

# socket hôte A
sock_A = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # mode UDP
# on lie le socket A à une adresse du réseau de rebouclage et un port whatever
sock_A.bind(("127.0.0.2", 6653))

# on essaie de se "connecter" au socket du client1
# en mode UDP ça définit l'adresse de destination par défaut pour les opérations send()
try:
    sock_A.connect(("127.0.0.1", 5653))
except:
    print("FAIL")
    exit()

# tant qu'on veut envoyer des messages
while True:
    data = input("entrez un message")
    if data:
        # peut utiliser send ici car on a configuré notre destinataire par défaut avec le connect plus haut
        sock_A.send(str.encode(data, encoding="utf-8"))

        if data == "quit":
            sock_A.shutdown(socket.SHUT_RDWR) # pas vraiment nécessaire pour UDP
            sock_A.close() # on ferme le socket
            break