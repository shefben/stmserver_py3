import threading, logging, struct, binascii, time, socket, ipaddress, os.path, ast

from Crypto.Hash import SHA

import steam
from . import config

class vttserver(threading.Thread):
    def __init__(self, xxx_todo_changeme, config) :
        (socket, address) = xxx_todo_changeme
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.config = config

    def run(self):
        log = logging.getLogger("vttsrv")

        clientid = str(self.address) + ": "

        log.info(clientid + "Connected to VTT Server")
        
        error_count = 0
        
        while True :
            try :

                #config_update = read_config()

                command = self.socket.recv(26)
                
                log.debug("COMMAND :" + binascii.b2a_hex(command) + ":")
                
                if command[0:8] == "\x53\x45\x4e\x44\x4d\x41\x43\x20" : #SENDMAC (v2) + MAC in caps and hyphens
                    #print("SENDMAC")
                    log.info(clientid + "SENDMAC received")
                    macaddress = binascii.unhexlify(binascii.b2a_hex(command))[9:26]
                    log.info(clientid + "MAC address received: " + macaddress)
                    #TO DO: create MAC filter here
                    
                    if self.config["cafe_use_mac_auth"] == "1" :
                        mac_count = 0
                        cafemacs = (self.config["cafemacs"].split(";"))
                        #print(len(cafemacs))
                        while mac_count < len(cafemacs) :
                            #print(cafemacs[mac_count])
                            if macaddress == cafemacs[mac_count] :
                                self.socket.send("\x01\x00\x00\x00") #VALID
                                break
                            mac_count = mac_count + 1
                            if mac_count == len(cafemacs) :
                                self.socket.send("\xfd\xff\xff\xff") #NO VALID MAC
                                break
                    else :
                        self.socket.send("\x01\x00\x00\x00") #ALWAYS VALID
                        
                elif command[0:6] == "\x53\x45\x54\x4d\x41\x43" : #SETMAC (v1)
                    log.info(clientid + "SETMAC received")
                    self.socket.send("\x01\x00\x00\x00")
                        
                elif command[0:4] == "\x00\x00\xff\xff" : #Response (v1)
                    log.info(clientid + "RESPONSE sent")
                    self.socket.send("\x01\x00\x00\x00") #INCORRECT AND UNKNOWN FOR 1.4
                        
                elif command[0:9] == "\x43\x48\x41\x4c\x4c\x45\x4e\x47\x45" : #CHALLENGE (v1)
                    log.info(clientid + "CHALLENGE received")
                    self.socket.send("\xff\xff\x00\x00") #CHALLENGE reply (can be anything, is the inverse of the client reply)
                    
                elif command[5:12] == "\x47\x45\x54\x49\x4e\x46\x4f" : #GETINFO
                    #print(binascii.b2a_hex(command))
                    log.info(clientid + "GETINFO received")
                    cafeuser = self.config["cafeuser"]
                    cafepass = self.config["cafepass"]
                    username_dec = cafeuser + "%" + cafepass
                    username_enc = steam.textxor(username_dec)
                    #print(username_dec)
                    #print(username_enc)
                    reply = struct.pack("<L", len(username_enc)) + username_enc
                    #print(binascii.b2a_hex(reply))
                    self.socket.send(reply)
                    
                elif command[0:8] == "\x53\x45\x4e\x44\x4d\x49\x4e\x53" or command[5:13] == "\x53\x45\x4e\x44\x4d\x49\x4e\x53" : #SENDMINS
                    log.info(clientid + "SENDMINS received")
                    #self.socket.send("\x01\x00\x00\x00") #FAKE MINS
                    reply = struct.pack("<L", int(self.config["cafetime"]))
                    self.socket.send(reply)
                    
                elif command[0:8] == "\x47\x45\x54\x49\x4e\x46\x4f\x20" : #GETINFO AGAIN
                    #print(binascii.b2a_hex(command))
                    log.info(clientid + "GETINFO received")
                    cafeuser = self.config["cafeuser"]
                    cafepass = self.config["cafepass"]
                    username_dec = cafeuser + "%" + cafepass
                    username_enc = steam.textxor(username_dec)
                    #print(username_dec)
                    #print(username_enc)
                    reply = struct.pack("<L", len(username_enc)) + username_enc
                    #print(binascii.b2a_hex(reply))
                    self.socket.send(reply)
                        
                elif command[0:8] == "\x50\x49\x4e\x47\x20\x20\x20\x20" : #PING
                    log.info(clientid + "PING received")
                
                elif len(command) == 5 :
                    log.warning(clientid + "Client failed to log in")
                
                elif len(command) == 0 :
                    log.info(clientid + "Client ended session")
                    break
                
                else :
                    if error_count == 1 :
                        log.info(clientid + "UNKNOWN VTT COMMAND " + binascii.b2a_hex(command[0:26]))
                    error_count = error_count + 1
                    if error_count > 5 :
                        #log.info(clientid + "CAS client logged off or errored, disconnecting socket")
                        break
                    
            except :
                log.error(clientid + "An error occured between the client and the VTT")
                break

        self.socket.close()
        log.info(clientid + "Disconnected from VTT Server")