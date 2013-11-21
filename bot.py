#Peter Gicking, 11/18/13 
#irc handle: swook


import socket
import sys

with open("test.txt", "wt") as out_file:
        out_file.write("This stuff goes out\nout!")

server = 'iss.cat.pdx.edu'       #settings
channel = '#swookbot'
botnick = 'swookbot'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 					#defines the socket
print('connecting to:'+server)
irc.connect((server, 6667))                                    				#connects to the server
irc.send('USER '+ botnick +' '+ botnick +' '+ botnick +' :Swooks Bot\n')    #user authentication
irc.send('NICK '+ botnick +'\n')                            				#sets nick
#irc.send("PRIVMSG nickserv :iNOOPE\r\n")    								#auth
irc.send('JOIN '+ channel +'\n')  											#join the chan
irc.send('PRIVMSG #swookbot :Successfully joined the channel\r\n')      				

while 1:    				#puts it in a loop
	text=irc.recv( 4096 ) 	#receive the text
	print(text)   			#print text to console
   
	if text.find('PING') != -1: #check if 'PING' is found
		irc.send('PONG \r\n')   #returns 'PONG' back to the server (prevents pinging out!

	if text.find( botnick + ': ping') != -1:
		irc.send('PRIVMSG ' + channel + ' :pong\r\n')
	
	if text.find( botnick + ': leave') != -1:
		irc.send('PRIVMSG ' + channel + '  :Leaving channel \r\n')
		irc.send('QUIT\r\n')
	
	if text.find( botnick + ': help') != -1:
		irc.send('PRIVMSG ' + channel + ' :Current commands: ping, leave, die, help\r\n')
		
	if text.find( botnick + ': source') != -1:
		irc.send('PRIVMSG ' + channel + ' :My source is at: https://github.com/pgicking/PythonIRC \r\n')
	
	if text.find(botnick + ': die') != -1:
		irc.send('PRIVMSG ' + channel + ' :Shutting down \r\n')
		irc.send('QUIT\r\n')
		break
