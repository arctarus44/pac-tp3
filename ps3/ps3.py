import os
import sys
import os.path
import random
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
from tools import *

PS3 = "/PS3"
PK = "/PK"
CHANGE = "/change"
SIGN = "/sign"
VALIDATE = "/validate"
SIGNATURE = "signature"
P = 'p'
G = 'g'
H = 'h'
M = 'm'
X = 'x'

PK_URL = PS3 + PK + NAME
CHANGE_PK_URL = PK_URL + CHANGE
SIGN_URL = PS3 + SIGN + NAME
VALIDATE_URL = PS3 + VALIDATE + NAME


def get_pubkey():
	"""Retrieve the public key of the PS3 on the server. Return a triplet
	of param (p, g, h)"""
	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(PK_URL)
	except clt.ServerError as err:
		print_serverError_exit(err)
	return result[P], result[G], result[H]

def sign(message):
	"""Sign a message using the server. The message must be an integer.
	Return the signature of the message as a tuple (r, s)"""

	if not isinstance(message, int):
		raise ValueError("The message must be an int !")

	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(SIGN_URL, {M : message})
	except clt.ServerError as err:
		print_serverError_exit(err)
	return result[SIGNATURE][0], result[SIGNATURE][1]

def change_pk():
	"""Ask a new public key to the server"""
	srv = clt.Server(BASE_URL)
	try:
		srv.query(CHANGE_PK_URL)
	except clt.ServerError:
		print_serverError_exit(err)

if __name__ == "__main__":
	p, g, h = get_pubkey()

	m0 = 123456
	m1 = 654321

	print("Génération des signatures")
	r, s0 = sign(m0)
	s1 = sign(m1)[1]

	q = p - 1

	print("Calcul de k")
	k = ((m0 - m1) * modinv((s0 - s1), q)) % q

	print("Calcul de x")
	x = (modinv(r, q) * (m0 - (k * s0))) % q

	if h == pow(g, x, p):
		print("La clé secréte calculé est bonne")
	else:
		print("La clé secréte calculé  n'est pas bonne.")
		exit(1)

	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(VALIDATE_URL, {X : x})
		print(result)
	except clt.ServerError as err:
		print_serverError_exit(err)
