#!/usr/bin/env python

import SocketServer

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

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
    #TODO: handle array of strings
    pass
  else:
    #TODO: handle single string
    pass
  
  

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

