import Utilitaires
import socket
import threeWayHandShake

#Fichier contenant le démarrage du serveur et son roulement

#Cration du socket et attente de connection
def ServeurStart(conf):
	port = 2212
	serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		serv_socket.bind((conf["IPv4"], port))
		print("Bind : Succes")
	except Exception as e:
		print("Bind : Echec, error: " + e)
		exit()
	threeWayHandShake.threeWay(conf, serv_socket)
	return serv_socket 

def main():
	print("L'adresse ipv4 de ce serveur est : 127.0.0.1")
	conf = Utilitaires.lectureConfigurationFile()
	serv_socket = ServeurStart(conf)

if __name__ == "__main__":
	main()
