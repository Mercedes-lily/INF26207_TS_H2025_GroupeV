#Fichiers de bases du coté Client
#Librairie pour utiliser les sockets

import socketFunction
import Utilitaires

#get nomFichier
#open ip
#str[0]  get      str[1]   nomFichier  str[2]
def lireEntree(client_socket):
    str = input("Veuillez entrer une commande:")
    strSplit = str.split()
    
    if(str.strip() == "ls"):
            print("ls")
            serv_adresse = ("127.0.0.1", 2212)
            str += "\r\n"
            client_socket.sendto(str.encode(), serv_adresse)
    elif (str.strip() == "bye"):
        print("bye")
        serv_adresse = ("127.0.0.1", 2212)
        str += "\r\n"
        client_socket.sendto(str.encode(), serv_adresse)
    elif(len(strSplit) == 2 and  strSplit[0] == "get"):
        print("get")
        serv_adresse = ("127.0.0.1", 2212)
        str = strSplit[0] + "\r\n" + strSplit[1] + "\r\n"
        client_socket.sendto(str.encode(), serv_adresse)
    elif(len(strSplit) == 2 and  strSplit[0] == "open"):
        print("open")
        serv_adresse = ("127.0.0.1", 2212)
        str = strSplit[0] + "\r\n" + strSplit[1] + "\r\n"
        client_socket.sendto(str.encode(), serv_adresse)
    else:
        print("Pas la bonne commande")

def main():
    isconnect = False
    conf = Utilitaires.lectureConfigurationFile()
    client_socket = socketFunction.SocketStart(conf, isconnect)
    lireEntree(client_socket)
    socketFunction.loop_client(isconnect)

if __name__ == "__main__":
    main()


# ls  --->    ls\r\n    get test.txt---->    get\r\ntest.txt\r\n