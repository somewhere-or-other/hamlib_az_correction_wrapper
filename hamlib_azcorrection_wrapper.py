#!/usr/bin/env python

import SocketServer
import re
import socket
import time
import sys
import pprint

extractAzEl_re = re.compile(r'^\s*[Pp]\s+([-.\d]+)\s+([-.\d]+)\s*$')


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

# StreamRequestHandler provides us with the rfile and wfile attributes
class EchoHandler(SocketServer.StreamRequestHandler):

    def log(self, peer, size):
        mapped = re.compile("^::ffff:", re.IGNORECASE)
        peer = re.sub(mapped, "", peer) # Clean IPv4-mapped addresses because I find
        # them confusing.
        sys.stdout.write("%s - %s - %i bytes\n" % (current_time(),
                                                   peer, size))
                                 
    def handle(self):
        """ Echoes (sends back) whatever it reads """
        # Warning, the Python read() is not the same as the C
        # read(). It operates on file objects, not sockets and has
        # different semantics.
        #
        # Just using read() will block until the TCP connection is
        # closed. We do not know the size in advance, hence the loop
        # with a size of 1. Now, you understand why HTTP has
        # Content-Length and why EPP-over-TCP prepends the length of
        # the XML element...
        #
        # Another solution would be to use self.request (the socket)
        # and to call recv(1024) and send() on it. Tests show that it
        # is *much* slower (twenty times slower on a local Ethernet).
        #
        data = "DUMMY"
        size = 0
        peer = self.client_address[0]
        while data != "":
            data = self.rfile.read(1)
            try:
                self.wfile.write(data)
                size = size + len(data)
            except socket.error: # Client went away, do not take that data into account
                data = ""
        self.log(peer, size)


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
                        return {'az': float(thismatch.groups()[0]), 'el': float(thismatch.groups()[1])}
        
        

if __name__ == "__main__":
        HOST, PORT = "localhost", 9999



        SocketServer.ThreadingTCPServer.allow_reuse_address = True
        # SocketServer should transparently accept IPv6 connections. But
        # it does not. So, we tell it. Note that using socket.AF_INET6
        # allows to receive *both* IPv4 and IPv6 (and, no, we cannot use
        # socket.AF_UNSPEC, it raises an exception :-( ), thanks to the
        # socket.IPV6_V6ONLY that we use in server_bind.
        
        # See the very detailed study
        # <https://edms.cern.ch/document/971407>
        SocketServer.ThreadingTCPServer.address_family = socket.AF_INET
        server = SocketServer.ThreadingTCPServer((HOST, PORT), EchoHandler)
        server.serve_forever()
    
