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
	Return the signature of the message"""

	if not isinstance(message, int):
		raise ValueError("The message must be an int !")

	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(SIGN_URL, {M : message})
	except clt.ServerError as err:
		print_serverError_exit(err)
	#TODO retourner un tuple correspondant aux deux valeurs de la signature elg
	return result[SIGNATURE]

if __name__ == "__main__":
	p, g, h = get_pubkey()
