import random

# Fonction qui vérifie si on peut envoyer un paquet
# Return: True si on peut envoyer, False sinon
def canSend():
	if random.random() < 0:
		return False
	return True
