#!/usr/bin/env python3
#  coding: utf-8 
import socketserver
import http.server
from socket import *
import requests as req
import re
import sys
import codecs
from pathlib import Path
from email.utils import formatdate
import os
import urllib3
import time

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
HOST, PORT = "localhost", 8080

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n\n" % self.data)
        decodedData = self.data.decode('utf-8')
        #a request we cant handle
        if 'PUT' in decodedData or 'POST' in decodedData or 'DELETE' in decodedData:
            data = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.request.sendall(data.encode())
            return
      
        start = decodedData.find('GET') + 3
        end = decodedData.find('HTTP',start)
        
        fPath = "www" + decodedData[start:end].strip()
        filePath = Path(fPath) #dont print this crap
        
        if not filePath.exists():
            data = "HTTP/1.1 404 Not Found\r\n\r\n" 
        else:
            
           
            if filePath.suffix[1:] == 'html' or filePath.suffix[1:] == 'css': 
                
                dataC = str(codecs.open(filePath,'r').read())
                data = "HTTP/1.1 200 OK\r\n"
                data += "Content-Type: text/{}; charset=utf-8\r\n".format(filePath.suffix[1:])
            elif fPath[len(fPath)-1] == "/" :
                
                fPath = fPath + "index.html"
                filePath = Path(fPath)
                dataC = str(codecs.open(filePath,'r').read()) 
                data = "HTTP/1.1 200 OK\r\n"
                data += "Content-Type: text/html; charset=utf-8\r\n".format(filePath.suffix[1:])
            elif fPath[len(fPath)-1] != '/':
                fPath1 = fPath + "/index.html"
                filePath = Path(fPath)
                filePath1 = Path(fPath1)
                if not filePath1.exists():
                    data = "HTTP/1.1 404 Not Found\r\n" 
                    dataC = ""
                else: 
                    dataC = str(codecs.open(filePath1,'r').read())
                    data = "HTTP/1.1 301 Moved Permanently\r\n" 
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "Location:http://127.0.0.1:8080{}/\r\n".format(decodedData[start:end].strip())
                
            
            data += "Date:{}\r\n".format(formatdate(timeval=None, localtime=False, usegmt=True))
            data += "Content-Length: {}\r\n".format(len(dataC))
            data += "\r\n"
            data += dataC


        
        self.request.sendall(data.encode())
        
    
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    
    with socketserver.TCPServer((HOST, PORT), MyWebServer) as server:
        server.serve_forever()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

