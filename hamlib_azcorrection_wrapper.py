#!/usr/bin/env python

import SocketServer
import re
import socket
import time
import sys
import pprint


#much of the socket code based on http://www.bortzmeyer.org/files/echoserver.py, as of 13 July 2016

extractAzEl_re = re.compile(r'^\s*([Pp])\s+([-.\d]+)\s+([-.\d]+)\s*$')
match_re = re.compile(r'^\s*[Pp]')

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def log(self, peer, msg):
        mapped = re.compile("^::ffff:", re.IGNORECASE)
        peer = re.sub(mapped, "", peer) # Clean IPv4-mapped addresses because I find
        # them confusing.
        sys.stdout.write("%s - %s - %s\n" % (current_time(),
                                                   peer, msg))
                                 
    def handle(self):

        data = "DUMMY"
        size = 0
        peer = self.client_address[0]
        while data != "":
            #data = self.rfile.read(1)
            data = self.rfile.readline()
            self.log(peer, "Read line: %s" % data)
                        
            try: #try to parse data
                position = extractAzEl(data)
                try:
                    self.log(peer, "Extracted data: az: %f, el: %f" % (position['az'], position['el']))
                    if position['az'] < 0:
                        position['az'] = negativeToPositive(position['az'])
                    data_mod = assembleFromExtracted(position)
                    self.wfile.write(data_mod)
                    self.log(peer, "Wrote line: %s" % data_mod)
                    size = size + len(data_mod)
                except socket.error: # Client went away, do not take that data into account
                    data = ""

            except ValueError:#data didn't match
                try:
                    self.wfile.write(data)
                    self.log(peer, "Wrote line: %s" % data)
                    size = size + len(data)
                except socket.error: # Client went away, do not take that data into account
                    data = ""
                
            
        self.log(peer, "%i bytes" % size)


def negativeToPositive(inputAzimuth):
        if(inputAzimuth < 0):
                return (inputAzimuth+360)%360
        else:
                return inputAzimuth%360

def positiveToNegative(inputAzimuth):
        if(inputAzimuth > 180):
                return (inputAzimuth%360)-360
        else:
                return inputAzimuth%360
            
def assembleFromExtracted(extractedData):
    return "%s %f %f" % (extractedData['cmd'], extractedData['az'], extractedData['el'])

def extractAzEl(inputString = None):
        if inputString == None:
                raise ValueError
        elif '__iter__' in dir(inputString):
                #if a list of strings:
                #convert to equivalent single string
                oldInputString = inputString
                
                inputString = "\n".join(oldInputString)

        #handle single string, including multi-line strings
        thismatch = extractAzEl_re.match(inputString)
        if thismatch == None:
                        raise ValueError
        else:
                        return {'cmd':thismatch.groups()[0], 'az': float(thismatch.groups()[1]), 'el': float(thismatch.groups()[2])}
        

def getHamlibSocket(hostname="localhost", port=4533):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    #sock.setblocking(0)
    return sock

def getHamlibCurrentPosition(socket, socket_fh=None):
    if socket_fh == None:
        socket_fh = socket.makefile()
    
    socket.sendall("p\n")
    retval = {'cmd': 'p'}
    retval['az'] = socket_fh.readline()
    retval['el'] = socket_fh.readline()

    return retval

if __name__ == "__main__":

        hamlib_socket = getHamlibSocket()
        hamlib_socket_fh = hamlib_socket.makefile()
        
        #seek to -90/+270 azimuth, with 30 deg elevation
        hamlib_socket.sendall(assembleFromExtracted({'cmd':'P','az':positiveToNegative(270),'el':30}) + "\n")
        received = hamlib_socket_fh.readline()
        print "Debugging: received: %s" % received

        for i in range(1,10):
            pprint.pprint(getHamlibCurrentPosition(hamlib_socket))
            time.sleep(2)


        #HOST, PORT = "localhost", 9999

        #SocketServer.ThreadingTCPServer.allow_reuse_address = True

        #SocketServer.ThreadingTCPServer.address_family = socket.AF_INET
        #server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
        #server.serve_forever()
        
