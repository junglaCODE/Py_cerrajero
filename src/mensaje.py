import mongodb
import sys
import getpass
import time
import logos

#################################################################################################
#					 					MONGO DB VERIFICATIONS 									#
#################################################################################################
def msg_usuario_login(USER, OPTION = True):

	cont = 0

	while (cont<3):

		if(OPTION):
			print("El usuario " + USER + " no existe.")
			print("¿Desea agregar el usuario? S/N")
		else:
			print("\n¿Estas seguro de eliminar el usuario '"+USER+"'? S/N")

		option=input(">>> ") 
		print("")

		if (option is 'S' or option is 's'):
			if(OPTION):
				PASSWORD = validar_key_password()

				#VALIDATE NEW USER IN DB
				if (mongodb.add_user(USER, PASSWORD[1])):
					return True
				else:
					return False
			else:
				mongodb.delete_user(USER)
				print("El usuario se elimino correctamente.\n")
				input('Preciona ENTER para continuar...')		
				print("")
				salir_cerrajero()

		elif (option is 'N' or option is 'n'):
			salir_cerrajero()
		else:
			print("Error opcion no valida.\n")
			cont = cont +1

	salir_cerrajero()

def msg_password():
	cont = 0
	while (cont<3):
		PASSWORD =getpass.getpass("Ingresa contraseña:")

		#CHECKING IF PASSWORD IS CORRECT
		EXIST = mongodb.exist_password(PASSWORD)
		if (EXIST):
			return True
		else:
			cont = cont + 1
			print("[ERROR]: Contraseña incorrecta, vuelve a intentarlo.\n")

	print("Ha exedido el numero de intentos.\n")
	input('Preciona ENTER para continuar...')	
	print("")		
	return False

def msg_password_master():
	cont = 0
	while (cont<3):
		PASSWORD =getpass.getpass("Ingresa contraseña:")

		#CHECKING IF PASSWORD IS CORRECT
		EXIST = mongodb.exist_password_master(PASSWORD)
		if (EXIST):
			return True
		else:
			cont = cont + 1
			print("[ERROR]: Contraseña incorrecta, vuelve a intentarlo.\n")

	print("Ha exedido el numero de intentos.\n")
	input('Preciona ENTER para continuar...')			
	return False	
#################################################################################################

#################################################################################################
#					 							MENU		 									#
#################################################################################################
def msg_welcome(USER):

	print("      =================================================")
	print(" =========== ¡Welcome to Cerrajero "+ USER + "! ==================")
	print("      =================================================")

	#SAVING OPTIONS IN A LIST
	option_name = ["Agregar llave", "Ver llaves", "Ver valor de llave", "Modificar llave", "Eliminar llave"
	,"Salir de cerrajero"]
	

	while True:
		cont = 1
		print("\n     °°°°°°°°° O P C I O N E S °°°°°°°°°°\n")
		#PRINTING OPTIONS
		for x in option_name:
			print("     "+str(cont) + ") " + option_name[cont-1] + ".")
			cont = cont + 1

		#CAPTURING OPTION (JUST NUMBERS)
		try:
			#INT(INPUT()) FOR TRY TO GET AN INTEGER NUMBER OPTION
			print("\n     °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
			option = int(input("Ingresa una opción (#):\n>>"))

			#CHECKING VALID OPTION
			if (option):
				if (option>0 and option <7):
					return (option, option_name[option-1])

			print("\nOpcion inválida, vuelve a intentarlo.")
		except ValueError: #IF USER DOESN'T TYPE A NUMBER SEND AN ERROR
			print("\n[ERROR]: Solo se aceptan números enteros.")
#################################################################################################

#################################################################################################
#					 					CERRAJERO FUNCTIONS 									#
#################################################################################################
def msg_key(USER, TEXT_OPTION = "", OPTION = "AGREGAR", NAME_KEY = "NULL", USER_PASSWORD = "NULL"):

	while True:
		KEY_NAME = input("Ingresa el nombre de la llave " + TEXT_OPTION + " [Default: Fecha]: ")
		if KEY_NAME=="":#ASIGN DEFAULT VALUE
			KEY_NAME = time.strftime("%Y-%m-%d") + " / " +time.strftime("%H:%M:%S")

		#VALIDATING KEY NAME IF EXIST
		if(mongodb.key_exist(USER, KEY_NAME)):
			print("\nLa llave ya se encuentra en existencia, intenta con otro nombre.\n")
		else:
			break
						
	PASSWORD = validar_key_password(EXIT = 0) #[0] argument confirm if passwords are the same

	if(PASSWORD[0]):#SO PASSWORD[1] CONTAIN THE TRUE PASSWORD
		DESCRIPCION = input("Descripción [Default: N/A]: ")

		if DESCRIPCION=="":
			DESCRIPCION = "N/A"

		if(OPTION=="AGREGAR"):
			mongodb.add_key(KEY_NAME, PASSWORD[1], DESCRIPCION, USER)
			input('\nPreciona ENTER para continuar...')
		else:
			mongodb.modified_key(USER, USER_PASSWORD, NAME_KEY, KEY_NAME, PASSWORD[1], DESCRIPCION)
			input('\nPreciona ENTER para continuar...')

def msg_modify_key(USER):
	mongodb.show_keys(USER);
	FIELDS = give_key_password("modificar")#[0] NAME_KEY / [1] USER_PASSWORD
	print("")
	if(mongodb.check_key_password(FIELDS[0], USER, FIELDS[1])):
		msg_key(USER, TEXT_OPTION = "",OPTION = "MODIFICAR", 
			NAME_KEY = FIELDS[0], USER_PASSWORD = FIELDS[1])
	else:
		input('\nPreciona ENTER para continuar...')
		
def msg_show_keys(USER):
	print("LLAVES:\n")
	mongodb.show_keys(USER)
	input('\nPreciona ENTER para continuar...')

def msg_show_key(USER):
	mongodb.show_keys(USER);
	FIELDS = give_key_password("desencriptar")#[0] NAME_KEY / [1] USER_PASSWORD
	mongodb.get_key(FIELDS[0], USER, FIELDS[1])	

def msg_delete_key(USER):
	mongodb.show_keys(USER)
	FIELDS = give_key_password("eliminar")#[0] NAME_KEY / [1] USER_PASSWORD
	mongodb.delete_key(FIELDS[0], USER, FIELDS[1])
	input('\nPreciona ENTER para continuar...')			

def give_key_password(OPTION):
	NAME_KEY = input("\nIngresa el nombre de la llave que deseas " + OPTION + ": ")
	USER_PASSWORD = getpass.getpass("Ingresa tu contrasena de usuario:")

	return (NAME_KEY, USER_PASSWORD)	

def msg_delete_user(USER):
	msg_usuario_login(USER, OPTION = False)

#################################################################################################

#################################################################################################
#					 						EXTRA FUNCTIONS 									#
#################################################################################################
def validar_key_password(CONT = 0, EXIT = 1):
	CONT = 0
	while (CONT < 3):
		password1=getpass.getpass("Teclee su contraseña: ")
		password2=getpass.getpass("Repite la contraseña: ")	
		CONT = CONT + 1
		#VALIDANDO CONTRASEÑAS VACIAS
		if password1!="":
			if ( password1 == password2 ):
				return (True,password1)
			else:
				print("\nLas contraseñas no coinciden, vuelve a intentarlo.\n")
		else:
			print("\nNo se admiten contraseñas vacías.\n")

	print("Ha exedido el numero de intentos.\n")
	input('Preciona ENTER para continuar...')
	print("")
	if(EXIT == 1):
		salir_cerrajero()
	else:
		return (False,"ERROR")

def salir_cerrajero():
	logos.logo_cerrajeroEND()
	sys.exit(0)

def encabezado():
	print("*******************************************************************************")
	print("       ********************** P a s s w o r d s ***********************")
	print("*******************************************************************************\n")
#################################################################################################