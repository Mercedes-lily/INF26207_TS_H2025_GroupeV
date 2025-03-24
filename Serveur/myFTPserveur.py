import Utilitaires
import socket
import threeWayHandShake
import Commandes
#Fichier contenant le démarrage du serveur et son roulement

#Creation du socket et attente de connection
def ServeurStart(conf):
	port = 2212
	serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		serv_socket.bind((conf["IPv4"], port))
		print("Bind : Succes")
	except Exception as e:
		print("Bind : Echec, error: " + e)
		exit()
	return serv_socket 

def connected_loop(serv_socket, conf):
	while True:
		try:
			data, client_adresse = serv_socket.recvfrom(int(conf["DataSize"]))  # Recoit jusqua DataSize bytes
			print(f"Received data from {client_adresse}: {data.decode()}")
			if(data.decode().strip(" \r\n") == "ls"):
				Commandes.handle_ls_command(client_adresse, serv_socket)
			if(data.decode().strip(" \r\n") == "bye"):
				Commandes.handle_bye_command(client_adresse, serv_socket)
				return
		except socket.timeout:
			pass  # Ignorer les délais d'attente et continuer à écouter

def main():
	print("L'adresse ipv4 de ce serveur est : 127.0.0.1")
	conf = Utilitaires.lectureConfigurationFile()
	try:
		serv_socket = ServeurStart(conf)
		serv_socket.settimeout(0.1) #On met le timeout a 0.1 pour ne pas bloquer le serveur et permettre une détection rapide de ctrl+c pour interrompre le serveur
		while True:
			threeWayHandShake.threeWay(conf, serv_socket)
			connected_loop(serv_socket, conf)
	except KeyboardInterrupt:
		print("Interruption du serveur par l'utilisateur (Ctrl+C)")

if __name__ == "__main__":
	main()
