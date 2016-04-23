from pymongo import MongoClient
import mongodb
import getpass
import mensaje
import sys
import logos

#FUNCTION TO EXECUTE THE PROGRAM
def run_cerrajero(USER):
	option = -1
	while option!=0:
		#OPTIONS
		option = mensaje.msg_welcome(USER)#GETTING OPTION
		print("\nOpción " + str(option[0]) + " - " + str(option[1]) + ":\n")

		#TASK FOR EACH OPTION
		if option[0]==1:#ADDING NEW KEY
			mensaje.msg_key(USER)
		elif option[0]==2:#SHOW KEYS
			mensaje.msg_show_keys(USER)
		elif option[0]==3:#SHOW KEY VALUE
			mensaje.msg_show_key(USER)
		elif option[0]==4:#MODIFY KEY
			mensaje.msg_modify_key(USER)
		elif option[0]==5:#DELETE_KEY
			mensaje.msg_delete_key(USER)
		elif option[0]==6:#EXIT CERRAJERO
			mensaje.salir_cerrajero()
		else:#DO NOTHING
			print	
logos.logo_cerrajero()

#FUNCTIONS ARGUMENTS
if(len(sys.argv)>1):
	if(sys.argv[1]=='USER' and len(sys.argv)>2):
		if(mongodb.user_exist(sys.argv[2])):
			if(mensaje.msg_password_master()):
				mensaje.msg_delete_user(sys.argv[2])
			else:
				print("")
				mensaje.salir_cerrajero()
		else:
			if (mensaje.msg_usuario_login(sys.argv[2])):
				run_cerrajero(sys.argv[2])
	elif(sys.argv[1]=='LOGIN' and len(sys.argv)>2):
		if(mongodb.user_exist(sys.argv[2])):
			if (mensaje.msg_password()):
				run_cerrajero(sys.argv[2])
			else:
				print("")
				mensaje.salir_cerrajero()
		else:
			print("[ERROR]: No se encontro el usuario especificado.")
			input('\nPreciona ENTER para continuar...')
			print("")
			mensaje.salir_cerrajero()	

#RUNNING CERRAJERO

# Get client from mongodb
client = MongoClient()

# Get USER
USER = getpass.getuser()

# Check USER
if (mongodb.user_exist(USER)):
	if (mensaje.msg_password()):
		run_cerrajero(USER)
	else:
		mensaje.salir_cerrajero()
else:
	#ADD USER?
	if (mensaje.msg_usuario_login(USER)):
		run_cerrajero(USER)
		
##3_0f*QVe;mJPHdxpw?S5yUTPpu!?4]j6B<A8-C<r}#cDQGjj_)9*xoCP]|HQejRsVD%#)kq=i2h