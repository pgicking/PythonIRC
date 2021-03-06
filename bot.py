#Peter Gicking, 11/18/13 
#irc handle: swook

#run command as python boy.py "channel key"

#TODO: Get nick of someone talking to bot
#TODO: re-write everything with twisted library
#TODO: Get X is Y command to work

import socket
import sys
import ConfigParser
import re
import sys
import ssl
import pickle

Config = ConfigParser.ConfigParser()
Config.read("config.txt")



#borrowed from https://wiki.python.org/moin/ConfigParserExamples
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
       print dict1
       return dict1
        

server = 'iss.cat.pdx.edu'                                                  #settings
NameFile = ConfigSectionMap("SectionOne")['namefile']                       #Sets the name of the text file that holds aliases in config.txt
channel = ConfigSectionMap("SectionOne")['channel']                         #Sets channel from config.txt
botnick = ConfigSectionMap("SectionOne")['botnick']                         #sets botnick from config.txt
channelkey = str(sys.argv[1])                                               #Set the passkey in arguments so its not publically availible in github


def addalias(s1,s2):
    print s1 + ' ' + s1
    null = { "blah"}
    pickle.dump(null,open(NameFile,"wb"))
    with open(NameFile, 'rb+') as fp:
#        content = fp.readlines()
        content = pickle.load(fp)
        print content
        if s1 in content:                                  #If s1 exists
            for n,i in enumerate(content):                                  #enum and find it
                if i == s1:                                                 #if its found
                    string = a[n]                                           #read it into 'string'
                    string = string + ' or ' + s2                           #append to string
                    a[n] = string                                           #replace with new string
        else:                                                               
            content.add(s1 + ' is ' + s2)
        pickle.dump(content,fp)
#        fp.write(content)                                               #write to the file



def send(text):
    irc.send('PRIVMSG ' + channel + ' :' + text + '\r\n')

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  #defines the sockets


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

    if text.find( botnick + ': ping') != -1:                #Returns p0ng
        send('p0ng')

    m = re.search(r'set (.*) to (.*)',text)
    if m:
        f1 = m.group(1)
        f2 = m.group(2)
        send('You said ' + f1 + ' to ' + f2)
        addalias(f1,f2)

    if text.find( botnick + ': help') != -1:                #Returns list of commands
        send('Current commands: ping, source, die, help')
        
    if text.find( botnick + ': source') != -1:              #Returns link to source
        send('My source is at: https://github.com/pgicking/PythonIRC')
    
    if text.find(botnick + ': die') != -1:                  #Kills bot
        if text.find('swook') != -1:                        #Only supposed to work for swook but its not yet working
            send('Shutting down')
            irc.send('QUIT\r\n')
            break
        else:
            send('You\'re not my real dad!')
