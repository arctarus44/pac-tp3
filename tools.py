NAME = "/dewarumez"
BASE_URL = "http://pac.bouillaguet.info/TP3"

AFF_ERROR = "Error no {0} : {1}"

def print_serverError_exit(err):
	print(AFF_ERROR.format(err.code, err.msg))
	exit(1)
