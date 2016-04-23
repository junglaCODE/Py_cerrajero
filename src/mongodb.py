from pymongo import MongoClient
from texttable import Texttable
from pyDes import *
import datetime
import hashlib
import time
import mensaje

#################################################################################################
#										MONGODB ATTRIB'S 										#
#################################################################################################

# CREATE CONNECTION TO MONGODB
client = MongoClient()
db = client.Cerrajero

# DEFINE COLLECTIONS
collection_master_key = db.Masterkey
collection_keys = db.Keys
#################################################################################################

#################################################################################################
#									VALIDATIONS TO MONGODB										#
#################################################################################################

def user_exist(USER):
	USER = collection_master_key.find_one({"user": USER})
	if USER:
		return True
	else:
		return False

def key_exist(USER, NAME):
	NAME = collection_keys[USER].find_one({"nombre": NAME})
	if NAME:
		return True
	else:
		return False		

def exist_password(PASSWORD):
	PASSWORD = collection_master_key.find_one({"password": hash_function(PASSWORD)})
	if PASSWORD:
		return True
	else:
		return False		

def exist_password_master(PASSWORD):
	PASSWORD = hash_function(PASSWORD)
	CURSOR = collection_master_key.find_one({"user":"CERRAJERO_MASTER_KEY"})
	if PASSWORD==CURSOR['password']:
		return True
	else:
		return False			

#################################################################################################

#################################################################################################
#										 HASH & CYPHER	 										#
#################################################################################################

#HASH FUNCTIONS
def hash_function(TEXT):
	TEXT = bytes(TEXT, 'utf-8')
	return (hashlib.md5(TEXT).hexdigest())

def hash_function_sha1(TEXT):
	TEXT = bytes(TEXT, 'utf-8')
	return (hashlib.sha1(TEXT).hexdigest())	

#ENCRYPT FUNCTIONS
def crypt_tripe_des(KEY_DES, KEY):
	KEY_DES = bytes(KEY_DES, 'utf-8')
	DES = triple_des(KEY_DES, CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)

	return DES.encrypt(KEY)

def decrypt_triple_des(KEY_DES, KEY):
	KEY_DES = bytes(KEY_DES, 'utf-8')
	DES = triple_des(KEY_DES, CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
	
	return DES.decrypt(KEY)

def get_key_crypt(USER):
	CURSOR = collection_master_key.find_one({"user":USER})

	KEY = hash_function_sha1(str(CURSOR['password']) + str(CURSOR['hash']))

	return generate_key(KEY)

def generate_key(KEY):
	KEY_DES = ""
	cont = 0

	while cont<len(KEY):
		KEY_DES = KEY_DES+KEY[cont]
		cont = cont + 2

	return "0x21"+KEY_DES
#################################################################################################

#################################################################################################
#										CERRAJERO FUNCTIONS										#
#################################################################################################

def add_user(USER, PASSWORD):
	PASSWORD = hash_function(PASSWORD)
	#DATE = time.strftime("%Y-%m-%d") + " / " +time.strftime("%H:%M:%S")
	DATE = hash_function_sha1(PASSWORD+USER)
	data = { "user": USER,
			 "password": PASSWORD,
			 "hash": DATE}

	data_id = collection_master_key.insert_one(data).inserted_id
	
	if (data_id):
		print("\nEl usuario " + USER + " ha sido agregado exitosamente.")
		input('\nPreciona ENTER para continuar...')
		clear_screen()
		return True
	else:
		print("\nEl usuario " + USER + " no se pudo agregar.")
		return False

def add_key(NAME, PASSWORD, DESCRIPTION, USER, OPTION = "AGREGAR"):
	#print(get_key_crypt(USER))
	PASSWORD = crypt_tripe_des(get_key_crypt(USER),PASSWORD)
	
	data = { "nombre": NAME,
			 "key": PASSWORD,
			 "descripcion": DESCRIPTION}

	data_id = collection_keys[USER].insert_one(data).inserted_id

	if (data_id):
		if(OPTION == "AGREGAR"):
			print("\nLa llave ha sido agregada con exito.")
		else:
			print("\nLa llave ha sido actualizada con exito.")
	else:
		print("\n[ERROR 0x01]: No se pudo agregar la llave.")			

def show_keys(USER):
	mensaje.encabezado()
	table = Texttable()
	keys = collection_keys[USER].find()
	table.add_row(["Nombre", "Valor", "Descripcion"])

	if(keys):
		for keys_field in keys:
			table.add_row([str(keys_field['nombre']), repr(keys_field['key']), str(keys_field['descripcion'])])

	print(table.draw())

def get_key(NAME_KEY, USER, PASSWORD):
	if(check_key_password(NAME_KEY, USER, PASSWORD, OPTION = True)):
		input('\nPreciona ENTER para continuar...')
	else:
		input('\nPreciona ENTER para continuar...')

def delete_key(NAME_KEY, USER, PASSWORD):
	if(check_key_password(NAME_KEY, USER, PASSWORD)):
		collection_keys[USER].find_one_and_delete({"nombre": NAME_KEY})
		print("\nLa llave " + NAME_KEY + " ha sido eliminada de la lista.")	

def modified_key(USER, USER_PASSWORD, NAME_KEY_PREVIEW, NAME_KEY, KEY, DESCRIPTION):
	collection_keys[USER].find_one_and_delete({"nombre": NAME_KEY_PREVIEW})
	add_key(NAME_KEY, KEY, DESCRIPTION, USER, OPTION = "MODIFICAR")

def delete_user(USER):
		collection_master_key.find_one_and_delete({"user": USER})

#################################################################################################

#################################################################################################
#					 					EXTRA FUNCTIONS 										#
#################################################################################################

#CLEAR SCREEN
def clear_screen(CONT = 0):
	CONT = 0
	while(CONT<25):
		print("")
		CONT = CONT+1

def check_key_password(NAME_KEY, USER, PASSWORD, OPTION = False):

	key = collection_keys[USER].find_one({"nombre": NAME_KEY})

	if key:
		PASSWORD = hash_function(PASSWORD)
		CURSOR = collection_master_key.find_one({"user":USER})

		if PASSWORD==CURSOR['password']:
			if(OPTION):
				KEY_DES = generate_key(hash_function_sha1(PASSWORD+str(CURSOR['hash'])))
				print ("\n** {0:30} {1}".format("Nombre", "Valor"))
				print ("-> {0:30} {1}".format(NAME_KEY, decrypt_triple_des(KEY_DES, key['key']).decode("utf-8")))
				return True
			else:
				return True
		else:
			print("\n[ERROR]: La contrasena de usuario es incorrecta.")
			return False
	else:
		print("\n[ERROR]: La llave especificada no se encuentra en la lista de llaves.")
		return False

#################################################################################################