import socket
from xml.dom.minidom import parse, parseString
import time
from Region import Region
from TrainType import TrainType
from Train import Train
import logging

logger = logging.getLogger(__name__)

class StsConnector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.settimeout(5)
        self.simtime = None
        self.region = None
        self.trainlist = []
        try:
            self.sock.connect((host, port))
            logger.info(f"Connected to {host}:{port}")
        except Exception:
            logger.error('An error occured during connection to Stellwerksim!')
            self.sock.close()

    def __del__(self):
        self.sock.close()
        
    def send_message(self, message, tag):
        logger.debug('send message: ' + message)
        self.sock.sendall(message.encode())
        return self.receive_full_message(tag)

    def write_xml(self, tag, payload = None):
        xml = '<' + tag
        if payload is not None:
            for attr, value in payload:
                xml += ' ' + attr + '=\"' + value + '\"'
        xml += ' />\n'
        return xml
    
    def register(self, version):
        self.send_message(self.write_xml('register', [('name', 'SumOfDelay'), ('autor', 'archimedes'), ('version', version), ('protokoll', '1'), ('text', 'Delay overview of your signal box.')]), 'status')
        response = self.send_message('', 'status')
        if self.read_xml_single(response, 'status', 'code') == '220':
            # simtime
            simtimeTag = self.send_message(self.write_xml('simzeit', [('sender', str(round(time.time())))]), 'simzeit')
            self.simtime = self.read_xml_single(simtimeTag, 'simzeit', 'zeit')

            # region
            signalBoxInfo = self.send_message(self.write_xml('anlageninfo'), 'anlageninfo')
            self.region = Region(self.read_xml_single(signalBoxInfo, 'anlageninfo', 'name'), self.read_xml_single(signalBoxInfo, 'anlageninfo', 'region'))

            # train list
            self.generateTrainList()
        else:
            logger.error('Registration failed!')
            
    def read_xml_single(self, response, tag, attribute):
        return parseString(response).getElementsByTagName(tag)[0].getAttribute(attribute)

    #def read_xml_multi(self, response, tag, attribute):
    #    taglist = parseString(response).getElementsByTagName(tag)
    #    attributelist = []
    #    for a in taglist:
    #        attributelist.append(a.getAttribute(attribute))
    #    return attributelist

    def generateTrainList(self):
        trainsxml = self.send_message(self.write_xml('zugliste'), 'zugliste')
        trainTag = parseString(trainsxml).getElementsByTagName('zug')
        intermediateTrainList = []
        for tags in trainTag:
            zid = tags.getAttribute('zid')
            name = tags.getAttribute('name')
            traindetailsxml = self.send_message(self.write_xml('zugdetails', [('zid', zid)]), 'zugdetails')
            delay = int(self.read_xml_single(traindetailsxml, 'zugdetails', 'verspaetung'))
            visible = False
            if self.read_xml_single(traindetailsxml, 'zugdetails', 'sichtbar') == 'true':
                visible = True
            mytype = TrainType(name, self.region.country)
            intermediateTrainList.append(Train(zid, name, mytype.traintype, delay, visible))
        self.trainlist = intermediateTrainList
        return intermediateTrainList


    def receive_full_message(self, tag):
        buffer = ''
        logger.debug('----receiving message parts...----')
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            buffer += data
            logger.debug(buffer)
            # Check if the complete message is received
            # directly closing tag
            if tag == 'simzeit' or tag == 'anlageninfo' or tag == 'zugdetails':
                if buffer.endswith('***EOR***\n') or buffer.endswith(' />\n') or buffer.endswith('</status>\n'):
                    break
            # more tags
            else:
                if buffer.endswith('***EOR***\n') or buffer.endswith('</' + tag + '>\n') or buffer.endswith('</status>\n'):
                    break
        logger.debug('----buffer complete----')
        return buffer.replace('\n', '')
