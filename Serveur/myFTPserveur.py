#Fichiers de bases du coté Serveur
#Librairie pour utiliser les sockets
import Utilitaires
import socketFunction  

def main():
	print("L'adresse ipv4 de ce serveur est : 127.0.0.1")
	conf = Utilitaires.lectureConfigurationFile()
	serv_socket = socketFunction.ServeurStart(conf)
	socketFunction.loop_client(serv_socket)


if __name__ == "__main__":
	main()
