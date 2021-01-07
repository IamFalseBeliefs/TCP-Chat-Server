import threading
import socket

inp = raw_input

adminUsrNm = "Host"
adminPass = "Host"

host = inp("[----] Host IP to Run on: ")
port = int(inp("[----] Port to Run on: "))
addr = (host, port)

form = ('ascii')
size = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen(port)

clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			msg = message = client.recv(size)
			if msg.decode(form).startswith("KICK"):
				if nicknames[clients.index(client)] == "Host":
					name_to_kick = msg.decode(form)[5:]
					kick_user(name_to_kick)
				else:
					client.send("[SERVER] Only admin can execute commands".ecnode(form))
			elif msg.decode(form).startswith("BAN"):
				if nicknames[clients.index(client)] == "Host":
					name_to_ban = msg.decode(form)[4:]
					kick_user(name_to_ban)
					with open('black.txt', 'a') as f:
						f.write(name_to_ban + "\n")
					print("[BANNED] " + name_to_ban + " Was banned succesfully")
				else:
					client.send("[SERVER] Only admin can execute commands".ecnode(form))
			else:
				broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast("[----]" + nickname + " Left the chat".encode(form))
			nicknames.remove(nickname)
			break

def recieve():
	while True:
		client, address = server.accept()
		print("[CONNECTION] " + str(address))
		client.send('NICK'.encode(form))
		nickname = client.recv(size).decode(form)
		
		with open("black.txt", "r") as f:
			bans = f.readlines()
		
		if nickname + "\n" in bans:
			client.send("BAN".encode(form))
			client.close()
			continue
		
		if nickname == adminUsrNm:
			client.send('PASS'.encode(form))
			password = client.recv(size).encode(form)
		
			if password != adminPass:
				client.send('REFUSE'.encode(form))
				client.close()
				continue
		
		nicknames.append(nickname)
		clients.append(client)
		print("[NICKNAME] " + nickname)
		broadcast("\n[----] " + nickname + " Joined the chat".encode(form))
		client.send("\n[----] Connected to the server".encode(form))
		thread = threading.Thread(target = handle, args = (client,))
		thread.start()

def kick_user(name):
	if name in nicknames:
		name_index = nicknames.index(name)
		client_to_kick = clients[name_index]
		clients.remove(client_to_kick)
		client_to_kick.send("[SERVER] You were kicked by an admin".encode(form))
		client_to_kick.close()
		nicknames.remove(name)
		broadcast("[SERVER] " + name + "was kicked by an admin!".encode(form))

print("[RUNNING] Server is running on " + str(host) + ":" + str(port))
recieve()









