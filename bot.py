#Peter Gicking, 11/18/13 
#irc handle: swook


import socket
import sys

server = 'iss.cat.pdx.edu'       #settings
channel = '#swookbot'
botnick = 'swookbot'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print('connecting to:'+server)
irc.connect((server, 6667))                                                 #connects to the server
irc.send(bytes('USER '+ botnick +' '+ botnick +' '+ botnick +' :Swooks Bot\n','UTF-8')) 	#user authentication
irc.send(bytes('NICK '+ botnick +'\n','UTF-8'))                            #sets nick
#irc.send("PRIVMSG nickserv :iNOOPE\r\n")    				#auth
irc.send(bytes('JOIN '+ channel +'\n','UTF-8'))  							#join the chan
irc.send(bytes('PRIVMSG #swookbot :Successfully joined the channel\r\n','UTF-8'))      				

while 1:    				#puts it in a loop
	text=irc.recv( 4096 ) 	#receive the text
	print(text)   			#print text to console
   
	if text.find(bytes('PING','UTF-8')) != -1: #check if 'PING' is found
		irc.send(bytes('PONG \r\n', 'UTF-8'))  #returns 'PONG' back to the server (prevents pinging out!

	if text.find(bytes('?swookbot ping', 'UTF-8')) != -1:
		irc.send(bytes('PRIVMSG #swookbot :pong\r\n', 'UTF-8'))
	
	if text.find(bytes('?swookbot leave', 'UTF-8' )) != -1:
		irc.send(bytes('PRIVMSG #swookbot  :Leaving channel \r\n', 'UTF-8'))
		irc.send(bytes('QUIT\r\n','UTF-8'))
	
	if text.find(bytes('?swookbot die', 'UTF-8' )) != -1:
		irc.send(bytes('PRIVMSG #swookbot :Shutting down \r\n', 'UTF-8'))
		irc.send(bytes('QUIT\r\n' , 'UTF-8'))
		break