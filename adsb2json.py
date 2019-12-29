import pyModeS as pms
from pyModeS.extra.tcpclient import TcpClient
import json
import socket

class ADSBClient(TcpClient):

    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    configuration = {}

    def __init__(self, configurationFile=None):

        print("ADSB2JSON  © 2019, P5 Software, LLC")
        print("Implements https://github.com/junzis/pyModeS")

        if configurationFile == None:
            configurationFile = "config.json" # Use the default file if one wasn't specified
            print("Using default config.json")

        with open(configurationFile) as tmpFile:
            self.configuration = json.load(tmpFile)

        if 'debug' not in self.configuration:
            self.configuration['debug'] = False

        if self.configuration['debug'] == True:
            print("Debug mode active")

        self.socketServer.bind((self.configuration['listenAddress'], self.configuration['listenPort']))
        self.socketServer.listen()

        self.conn, self.addr = self.socketServer.accept() # Wait for a connection

        super(ADSBClient, self).__init__(self.configuration['serverName'], self.configuration['serverPort'], self.configuration['serverType'])

    def handle_messages(self, messages):

        for msg, ts in messages:

            if len(msg) != 28:  # wrong data length
                if self.configuration['debug'] != True:
                        continue

            #If CRC doesn't pass, exit the loop
            if pms.crc(msg) !=0:  # CRC fail
                if self.configuration['debug'] != True:
                        continue

            #Global data we can always expect
            downlinkFormat = pms.df(msg)

            #Object to store data
            data = {}

            if self.configuration['debug'] == True:
                data['DEBUG_MODE'] = True

            if self.configuration['debug'] == True:
                data['downlinkFormat'] = downlinkFormat
            
            #Throw away certain DF's (0 & 16 are ACAS, 11 is all-call)
            if downlinkFormat == 0 or downlinkFormat == 11 or downlinkFormat == 16:
                if self.configuration['debug'] != True:
                        continue

            data['timestamp'] = ts
            data['icaoAddress'] = pms.adsb.icao(msg)

            if downlinkFormat == 4 or downlinkFormat == 20:
                data['altitude'] = pms.common.altcode(msg)

            if downlinkFormat == 5 or downlinkFormat == 21:
                data['squawk'] = pms.common.idcode(msg) 

            if downlinkFormat == 17:
                
                typeCode = pms.adsb.typecode(msg)

                if self.configuration['debug'] == True:
                    data['typeCode'] = typeCode

                # Throw away TC 28
                if typeCode == 28 or typeCode == 29:
                    if self.configuration['debug'] != True:
                        continue

                if 1 <= typeCode <= 4:
                    data['callsign'] = pms.adsb.callsign(msg).replace("_","")
                    data['aircraftCategory'] = pms.adsb.category(msg)                    

                if 5 <= typeCode <= 18 or 20 <= typeCode <=22:
                    data['latitude'] = pms.adsb.position_with_ref(msg, self.configuration['latitude'], self.configuration['longitude'])[0]
                    data['longitude'] = pms.adsb.position_with_ref(msg, self.configuration['latitude'], self.configuration['longitude'])[1]
                    data['altitude'] = pms.adsb.altitude(msg)

                if 5 <= typeCode <= 8:
                    data['velocity'] = pms.adsb.velocity(msg)[0]
                    data['heading'] = pms.adsb.velocity(msg)[1]
                    data['verticalSpeed'] = pms.adsb.velocity(msg)[2]

                if typeCode == 19:
                    data['velocity'] = pms.adsb.velocity(msg)[0]
                    data['heading'] = pms.adsb.velocity(msg)[1]
                    data['verticalSpeed'] = pms.adsb.velocity(msg)[2]

                if typeCode == 31:
                    data['adsbVersion'] = pms.adsb.version(msg)

            try:
                if self.conn.fileno() != -1:
                    self.conn.sendall(json.dumps(data).encode('utf-8'))
                    self.conn.sendall("\n".encode('utf-8'))
            
            except:
                if self.configuration['debug'] == True:
                    print("[Debug] Connection Closed")
                self.conn.close()
                self.socketServer.listen()
                self.conn, self.addr = self.socketServer.accept() #Set the connection to accept connections again

# run new client, change the host, port, and rawtype if needed
client = ADSBClient()
client.run()