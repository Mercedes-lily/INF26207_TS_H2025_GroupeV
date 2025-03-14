#Fichiers de bases du coté Client
#Librairie pour utiliser les sockets

import socketFunction
import Utilitaires

def main():
    isconnect = False
    conf = Utilitaires.lectureConfigurationFile()
    client_socket = socketFunction.SocketStart(conf, isconnect)
    socketFunction.loop_client(isconnect)

    

if __name__ == "__main__":
    main()