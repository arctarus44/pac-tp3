import os
import sys
import os.path
import random
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
from tools import *
import math

ELGAMAL = "/ElGamal-encryption"
PARAM = "/parameters/"
CHALLENGE = "/challenge/"
VALIDATE = "/validate/"

PARAM_URL = ELGAMAL + PARAM + NAME
CHALLENGE_URL = ELGAMAL + CHALLENGE + NAME
VALIDATE_URL = ELGAMAL + VALIDATE + NAME

P = 'p'
G = 'g'
H = 'h'
CIPHERTEXT = "ciphertext"
PLAINTEXT = "plaintext"

def extended_gcd(aa, bb):
	lastremainder, remainder = abs(aa), abs(bb)
	x, lastx, y, lasty = 0, 1, 1, 0
	while remainder:
		lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
		x, lastx = lastx - quotient*x, x
		y, lasty = lasty - quotient*y, y
	return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


def get_param():
	"""Retrieve parameters used by elgamal.
	This first time may be quiet long. Be patient!
	Return the two parameters p and g."""
	srv = clt.Server(BASE_URL)
	try:
		param = srv.query(PARAM_URL)
		return param[P], param[G]
	except clt.ServerError as err:
		print_serverError_exit(err)

def gen_x(p):
	"""Pick a random int between 1 and p."""
	return random.randint(1, p-1)

def gen_h(g, x, p):
	"""Generate h"""
	return pow(g, x, p)

def decipher(a, b, x, p):
	h = pow(a, x, p)
	h_inv = modinv(h, p)
	decipher_text = (b * h_inv) % p
	return decipher_text

if __name__ == "__main__":
	p, g = get_param()

	x = gen_x(p)

	h = gen_h(g, x, p)

	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(CHALLENGE_URL, {H : h})
	except clt.ServerError as err:
		print_serverError_exit(err)

	a = result[CIPHERTEXT][0]
	b = result[CIPHERTEXT][1]

	plain = decipher(a, b, x, p)
	try:
		result = srv.query(VALIDATE_URL, {PLAINTEXT : plain})
		print(result)
	except clt.ServerError as err:
		print_serverError_exit(err)
