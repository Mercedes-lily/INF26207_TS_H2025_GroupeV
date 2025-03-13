#Fonction liés à l'envoie au Client

#TypeRequete\r\nVariable 1\r\nVariable 2\r\n ... \r\nVariable n\r\n\r\n
#TypeRequete\r\nVariable 1\r\nVariable 2\r\n ... \r\nVariable n\r\n\r\n

#Retour get
#Code Description\r\nTaille du Header\r\nTaille des données envoyées\r\nNuméro du bloc\r\nDonnées\r\n\r\n
#1 OK\r\nTailleHeader:37\r\nTaille:200000\r\nBloc:13\r\nDonnées:Données\r\n\r\n
#Code Description\r\nTaille du Header\r\nTaille des données envoyées\r\nNuméro du bloc\r\nDonnées\r\n\r\n
#1 OK\r\nTailleHeader:37\r\nTaille:200000\r\nBloc:13\r\nDonnées:Données\r\n\r\n

#Retour bye
#Code Description\r\n\r\n
#2 Fermeture OK\r\n\r\n
#Code Description\r\n\r\n
#2 Fermeture OK\r\n\r\n

#Retour ls
#Code Description\r\nTaille du Header\r\nTaille des données envoyées\r\nDonnées\r\n\r\n
#1 OK\r\nTailleHeader:37\r\nTaille:25000\r\nDonnées:socket.py\nModule1.pdf\r\n\r\n
#Code Description\r\nTaille du Header\r\nTaille des données envoyées\r\nDonnées\r\n\r\n
#1 OK\r\nTailleHeader:37\r\nTaille:25000\r\nDonnées:socket.py\nModule1.pdf\r\n\r\n

#Retour open (Ack-Syn)
#Code Description\r\nTaille du Header\r\nTaille Négociée\r\nNombre de morceaux maximales avant l'accusé de réception\r\n\r\n
#5 Ack-Syn\r\nTailleHeader:37\r\nTaille:30000\r\nNombreMorceaux:3\r\n\r\n
#Code Description\r\nTaille du Header\r\nTaille Négociée\r\nNombre de morceaux maximales avant l'accusé de réception\r\n\r\n
#5 Ack-Syn\r\nTailleHeader:37\r\nTaille:30000\r\nNombreMorceaux:3\r\n\r\n

#Retour Erreur
#Code Description\r\n\r\n
#0 Erreur\r\n\r\n

import random


# Fonction qui vérifie si on peut envoyer un paquet
# Return: True si on peut envoyer, False sinon
def canSend():
	if random.random() < 0.05:
		return False
	return True


if __name__ == '__main__':
	if canSend():
		sendPacket()