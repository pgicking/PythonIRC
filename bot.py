#Peter Gicking, 11/18/13 
#irc handle: swook

#run command as python boy.py "password"

#TODO: Get nick of someone talking to bot
#TODO: re-write everything with twisted library
#TODO: Get X is Y command to work

import socket
import sys
import ConfigParser
import re
import sys
import ssl


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
channel = ConfigSectionMap("SectionOne")['channel']                         #Sets channel from config.txt
botnick = ConfigSectionMap("SectionOne")['botnick']                         #sets botnick from config.txt
channelkey = str(sys.argv[1])                                               #Set the passkey in arguments so its not publically availible in github


def send(text):
    irc.send('PRIVMSG ' + channel + ' :' + text + '\r\n')

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  #defines the sockets


#irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                     #defines the socket
print('connecting to:'+server)
socket.connect((server,6697))                                               #Connects to the server
irc = ssl.wrap_socket(socket)
irc.send('USER '+ botnick +' '+ botnick +' '+ botnick +' :Swooks Bot\n')    #user authentication
irc.send('NICK '+ botnick +'\n')                                            #sets nick
#irc.send('JOIN ' + channel + '\n')
irc.send('JOIN '+ channel + ' ' + channelkey + '\n')                        #join the chan
send('Hello!')                                                              #Opening message

while 1:                    #puts it in a loop
    text=irc.recv( 4096 )   #receive the text
    print(text)             #print text to console
   
    if text.find('PING') != -1: #check if 'PING' is found
        irc.send('PONG \r\n')   #returns 'PONG' back to the server (prevents pinging out!

    if text.find( botnick + ': ping') != -1:
        send('p0ng')

#    if text.find( botnick + ': (.*)  is also (.*)' ) != -1:
#        irc.send( 'You said ' + nick + ' is ' + info + '\r\n') 

    if text.find( botnick + ': help') != -1:
        send('Current commands: ping, source, die, help')
        
    if text.find( botnick + ': source') != -1:
        send('My source is at: https://github.com/pgicking/PythonIRC')
    
    if text.find(botnick + ': die') != -1:
        send('Shutting down')
        irc.send('QUIT\r\n')
        break
