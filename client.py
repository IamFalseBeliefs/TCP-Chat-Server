import threading
import socket

inp = raw_input

adminUsrNm = "Host"

host = inp("[----] Host IP to connect to: ")
port = int(inp("[----] Port to connect to: "))
nickname = inp("[----] Please select a nickname for the server: ")

if nickname == adminUsrNm:
	password = inp("[----] Enter Admin password: ")


addr = (host, port)

form = ('ascii')
size = 2048

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

stop_thread = False

def receive():
	while True:

		global stop_thread

		if stop_thread:
			break

		try:
			message = client.recv(size).decode(form)

			if message == 'NICK':
				client.send(nickname.encode(form))
				next_message = client.recv(size).decode(form)
				
				if next_message == 'PASS':
					client.send(password.encode(form))
					
					if client.recv(size).decode(form) == 'REFUSE':
						print("[DISSCONNECTED] Wrong password")
						stop_thread = True
				
				elif next_message == "BAN":
					print("[SERVER] Connection refused due to perm-ban!")
					client.close()
					stop_thread = True

			else:
				print(str(message))
		except:
			print("[DISSCONNECTED]")
			client.close()
			break

def write():
	while True:
		if stop_thread:
			break

		message = nickname + ": " + inp("")
		
		if message[len(nickname) + 2:].startswith("/"):
			
			if nickname == "Host":
				
				if message[len(nickname) + 2].startswith("/kick"):
					client.send("KICK " + message[len(nickname) + 2 + 6].encode(form))
				
				elif message[len(nickname) + 4].startswith("/ban"):
					client.send("BAN " + message[len(nickname) + 2 + 5].encode(form))
			else:
				print("[----] Commands can only be executed by an Admin!")
		else:
			client.send(message.encode(form))

trcv = threading.Thread(target = receive)
trcv.start()

twrite = threading.Thread(target = write)
twrite.start()