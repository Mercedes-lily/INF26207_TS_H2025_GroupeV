#Fonction liés à l'envoie au serveur

#Format du Header par commande


#TypeRequete\r\nVariable 1\r\nVariable 2\r\n ... \r\nVariable n\r\n\r\n

#Envoie get
#Commande\r\nFichier demandé\r\nTaille du Header\r\n\r\n
#Get\r\nsocket.py\r\nTailleHeader:37\r\n\r\n

#Retour Accusées de reception
#Code Description\r\n\r\n
#4 Reception\r\n\r\n

#Envoi ls et bye
#Commande\r\n\r\n
#ls\r\n\r\n
#bye\r\n\r\n

#Envoie open (Syn)
#Commande\r\nadresse ip\r\nTaille du Header\r\nTaille proposé\r\nNombre de morceaux maximales avant l'accusé de réception proposé\r\n\r\n
#Open\r\n127.0.0.0\r\nTailleHeader:37\r\nTaille:30000\r\nNombreMorceaux:3\r\n\r\n

#Retour open (Ack)
#Code Description\r\nTaille du Header\r\nTaille accepté\r\nNombre de morceaux maximales avant l'accusé de réception accepté\r\n\r\n
#6 Ack\r\nTailleHeader:37\r\nTaille:30000\r\nNombreMorceaux:3\r\n\r\n

#Retour Erreur
#Code Description\r\n\r\n
#0 Erreur\r\n\r\n
import random


# Fonction qui vérifie si on peut envoyer un paquet
# Return: True si on peut envoyer, False sinon
def canSend():
	if random.random() < 0.75:
		return False
	return True
