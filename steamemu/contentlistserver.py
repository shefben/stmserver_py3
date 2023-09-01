import threading, logging, struct, binascii, os

import steam
from . import config
import globalvars

class contentlistserver(threading.Thread):
    def __init__(self, xxx_todo_changeme, config) :
        (socket, address) = xxx_todo_changeme
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.config = config

    def run(self):
        log = logging.getLogger("clstsrv")
        clientid = str(self.address) + ": "
        log.info(clientid + "Connected to Content List Server ")
        
        if self.config["public_ip"] != "0.0.0.0" :
            if clientid.startswith(globalvars.servernet) :
                bin_ip = steam.encodeIP((self.config["server_ip"], self.config["file_server_port"]))
            else :
                bin_ip = steam.encodeIP((self.config["public_ip"], self.config["file_server_port"]))
        else:
            bin_ip = steam.encodeIP((self.config["server_ip"], self.config["file_server_port"]))
        
        msg = self.socket.recv(4)
        if msg == b"\x00\x00\x00\x02" :
            self.socket.send(b"\x01")

            msg = self.socket.recv_withlen()
            command = msg[0]
            if command == 0x00 :
                if msg[2] == 0x00 and len(msg) == 21 :
                    log.info(clientid + "Sending out file servers with packages")
                    reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                elif msg[2] == 0x01 and len(msg) == 25 :
                    (appnum, version, numservers, region) = struct.unpack(">xxxLLHLxxxxxxxx", msg)
                    log.info("%ssend which server has content for app %s %s %s %s" % (clientid, appnum, version, numservers, region))

                    if os.path.isfile("files/cache/" +str(appnum) + "_" + str(version) + "/" +str(appnum) + "_" + str(version) + ".manifest") :
                        reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                    elif os.path.isfile(self.config["v2manifestdir"] + str(appnum) + "_" + str(version) + ".manifest") :
                        reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                    elif os.path.isfile(self.config["manifestdir"] + str(appnum) + "_" + str(version) + ".manifest") :
                        reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                    elif os.path.isdir(self.config["v3manifestdir2"]) :
                        if os.path.isfile(self.config["v3manifestdir2"] + str(appnum) + "_" + str(version) + ".manifest") :
                            reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                        else :
                            if self.config["sdk_ip"] == "0.0.0.0" :
                                log.warning("%sNo servers found for app %s %s %s %s" % (clientid, appnum, version, numservers, region))
                                reply = b"\x00\x00" # no file servers for app
                            else :
                                log.info("%sHanding off to SDK server for app %s %s" % (clientid, appnum, version))
                                bin_ip = steam.encodeIP((self.config["sdk_ip"], self.config["sdk_port"]))
                                reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                    else :
                        if self.config["sdk_ip"] == "0.0.0.0" :
                            log.warning("%sNo servers found for app %s %s %s %s" % (clientid, appnum, version, numservers, region))
                            reply = b"\x00\x00" # no file servers for app
                        else :
                            log.info("%sHanding off to SDK server for app %s %s" % (clientid, appnum, version))
                            bin_ip = steam.encodeIP((self.config["sdk_ip"], self.config["sdk_port"]))
                            reply = struct.pack(">H", 1) + b"\x00\x00\x00\x00" + bin_ip + bin_ip
                else :
                    log.warning("Invalid message! " + binascii.b2a_hex(msg))
                    reply = b"\x00\x00"
            elif command == 0x03 : # send out file servers (Which have the initial packages)
                log.info(clientid + "Sending out file servers with packages")
                reply = struct.pack(">H", 1) + bin_ip
            else :
                log.warning("Invalid message! " + binascii.b2a_hex(msg).decode())
                reply = ""
            self.socket.send_withlen(reply)
        else :
            log.warning("Invalid message! " + binascii.b2a_hex(msg).decode())

        self.socket.close()
        log.info(clientid + "Disconnected from Content List Server")
