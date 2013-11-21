#Peter Gicking, 11/18/13 
#irc handle: swook


import socket
import sys
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("config.txt")

with open("test.txt", "wt") as out_file:
        out_file.write("ttttttThis stuff goes out\nout!")

#Stolen from https://wiki.python.org/moin/ConfigParserExamples
def ConfigSectionMap(section):
       dict1 = {}
       options = Config.options(section)
       for option in options:
           try:
               dict1[option] = Config.get(section,option)
               if dict1[option] == -1:
                   DebugPrint("skip: %s" % option)
           except:
               print("exception on %s!" % option)
               dict1[option] = None
       return dict1
        

server = 'iss.cat.pdx.edu'       #settings
channel = ConfigSectionMap("SectionOne")['channel']
botnick = ConfigSectionMap("SectionOne")['botnick']



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
