import threading, logging, struct, binascii

import steam
import globalvars

class directoryserver(threading.Thread):
    def __init__(self, xxx_todo_changeme, config) :
        (socket, address) = xxx_todo_changeme
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.config = config

    def run(self):
        log = logging.getLogger("dirsrv")
        clientid = str(self.address) + ": "
        log.info(clientid + "Connected to Directory Server")
        
        #print("Client ID is: " + clientid)
        command = ''
        msg = self.socket.recv(4)
        log.debug(binascii.b2a_hex(msg))
        if msg == b"\x00\x00\x00\x01" :
            self.socket.send(b"\x01")

            msg = self.socket.recv_withlen()
            command = msg[0]
            log.debug(binascii.b2a_hex(command))
            if command == 0x00 : # send out auth server for a specific username
                log.info(clientid + "Sending out specific auth server: " + binascii.b2a_hex(command))
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                        #bin_ip = steam.encodeIP("172.21.0.20", "27039")
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["auth_server_port"]))
                        #bin_ip = steam.encodeIP("172.21.0.20", "27039")
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                    #bin_ip = steam.encodeIP("172.21.0.20", "27039")
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x03 : # send out config servers
                log.info(clientid + "Sending out list of config servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["conf_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["conf_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["conf_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x06 : # send out content list servers
                log.info(clientid + "Sending out list of content list servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["contlist_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["contlist_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["contlist_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x0f : # hl master server
                log.info(clientid + "Requesting HL Master Server")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        #bin_ip = steam.encodeIP(("172.20.0.23", self.config["hlmaster_server_port"]))
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27010))
                    else :
                        #bin_ip = steam.encodeIP(("172.20.0.23", self.config["hlmaster_server_port"]))
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27010))
                else :
                    #bin_ip = steam.encodeIP(("172.20.0.23", self.config["hlmaster_server_port"]))
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27010))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x12 : # account retrieve server address, not supported
                log.info(clientid + "Sending out list of account retrieval servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["auth_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x14 : # send out CSER server (not implemented)
                log.info(clientid + "Sending out list of CSER(?) servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27013))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27013))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27013))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x18 : # source master server
                log.info(clientid + "Requesting Source Master Server")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27011))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27011))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27011))
                #reply = struct.pack(">I", 8) + struct.pack(">H", 1) + bin_ip
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x1e : # rdkf master server
                log.info(clientid + "Requesting RDKF Master Server")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27012))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27012))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27012))
                #reply = struct.pack(">I", 8) + struct.pack(">H", 1) + bin_ip
                reply = struct.pack(">H", 1) + bin_ip
            else :
                log.info(clientid + "Invalid/not implemented command: " + binascii.b2a_hex(msg))
                reply = b"\x00\x00"

            self.socket.send_withlen(reply)

        elif msg == b"\x00\x00\x00\x02" :
            self.socket.send(b"\x01")

            msg = self.socket.recv_withlen()
            command = msg[0]
            log.debug(binascii.b2a_hex(bytes([command])))

            if command == 0x00 and len(msg) == 5 : # send out auth server for a specific username
                log.info(clientid + "Sending out specific auth server: " + binascii.b2a_hex(command))
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                        #bin_ip = steam.encodeIP(("172.21.0.20", "27039"))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["auth_server_port"]))
                        #bin_ip = steam.encodeIP(("172.21.0.20", "27039"))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                    #bin_ip = steam.encodeIP(("172.21.0.31", "28039"))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x03 : # send out config servers
                log.info(clientid + "Sending out list of config servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["conf_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["conf_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["conf_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x06 : # send out content list servers
                log.info(clientid + "Sending out list of content list servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["contlist_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["contlist_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["contlist_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x0b or command == 0x1c : # send out auth server for a specific username
                log.info(clientid + "Sending out auth server for a specific username: " + binascii.b2a_hex(command))
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["auth_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x0f : # hl master server
                log.info(clientid + "Requesting HL Master Server")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        #bin_ip = steam.encodeIP(("172.20.0.23", self.config["hlmaster_server_port"]))
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27010))
                    else :
                        #bin_ip = steam.encodeIP(("172.20.0.23", self.config["hlmaster_server_port"]))
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27010))
                else :
                    #bin_ip = steam.encodeIP(("172.20.0.23", self.config["hlmaster_server_port"]))
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27010))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x12 : # account retrieve server address, not supported
                log.info(clientid + "Sending out list of account retrieval servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], self.config["auth_server_port"]))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], self.config["auth_server_port"]))
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x14 : # send out CSER server (not implemented)
                log.info(clientid + "Sending out list of CSER servers")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27013))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27013))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27013))
                #reply = struct.pack(">I", 8) + struct.pack(">H", 1) + bin_ip
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x18 : # source master server
                log.info(clientid + "Requesting Source Master Server")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27011))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27011))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27011))
                #reply = struct.pack(">I", 8) + struct.pack(">H", 1) + bin_ip
                reply = struct.pack(">H", 1) + bin_ip
            elif command == 0x1e : # rdkf master server
                log.info(clientid + "Requesting RDKF Master Server")
                if self.config["public_ip"] != "0.0.0.0" :
                    if clientid.startswith(globalvars.servernet) :
                        bin_ip = steam.encodeIP((self.config["server_ip"], 27012))
                    else :
                        bin_ip = steam.encodeIP((self.config["public_ip"], 27012))
                else :
                    bin_ip = steam.encodeIP((self.config["server_ip"], 27012))
                #reply = struct.pack(">I", 8) + struct.pack(">H", 1) + bin_ip
                reply = struct.pack(">H", 1) + bin_ip
            else :
                log.info(clientid + "Invalid/not implemented command: " + binascii.b2a_hex(msg))
                reply = b"\x00\x00"

            self.socket.send_withlen(reply)
        
        else :
            log.error(clientid + "Invalid version message: " + binascii.b2a_hex(command.encode()).decode())


        self.socket.close()
        log.info (clientid + "disconnected from Directory Server")
