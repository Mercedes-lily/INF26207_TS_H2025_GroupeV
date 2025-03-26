#Fonction liés à l'envoie au Client

import random

# Fonction qui vérifie si on peut envoyer un paquet
# Return: True si on peut envoyer, False sinon
def canSend(fiabilite):
	if random.random() < (1-fiabilite): # X% de chance de ne pas envoyer le paquet si fiabilite = 0.95, alors 5% de chance de ne pas envoyer le paquet
		return False
	return True
