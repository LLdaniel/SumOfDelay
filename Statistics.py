import logging
logger = logging.getLogger(__name__)

class Statistics:
    def __init__(self):
        self.trains = set([])
        self.trainsInvisible = set([])
        self.delay = [0, 0, 0, 0, 0, 0, 0, 0]
        self.typemapping = ('FREIGHT', 'LONGDISTANCE', 'REGIONAL', 'CITY', 'SPECIAL', 'LOCO', 'CONSTRUCTION', 'OTHER')
        
    def add_train(self, train):
        index = self.find_index(train.traintype)
        if train.visible:
            self.trains.add(train)
        else:
            self.trainsInvisible.add(train)
        
    def find_index(self, ttype):
        index = -1
        for t in self.typemapping:
            index += 1;
            if t == ttype:
                break
        return index

    def add_delay(self, ttype, diff):
        index = self.find_index(ttype)
        self.delay[index] += diff
        
    def update(self, stsCon):
        # integrate updated trainlist into statistics lists
        self.trainsInvisible = set(stsCon.generateTrainList()) - self.trains

        # update new delay
        for i in self.trains.copy():
            traindetailsxml = stsCon.send_message(stsCon.write_xml('zugdetails', [('zid', str(i.tid))]), 'zugdetails')
            newdelay = int(stsCon.read_xml_single(traindetailsxml, 'zugdetails', 'verspaetung'))
            self.add_delay(i.traintype, i.diff(newdelay))
            
            # remove trains that have become invisible
            newvisible = False
            if stsCon.read_xml_single(traindetailsxml, 'zugdetails', 'sichtbar') == 'false':
                self.trains.remove(i)
                #i.visible = False
                #self.trainsInvisible.add(i) train completely gone? otherwise will be re-introduced with updated invisible listx
                
        # add newly visible to list and remove from invisible list
        for j in self.trainsInvisible.copy():
            traindetailsxml = stsCon.send_message(stsCon.write_xml('zugdetails', [('zid', str(j.tid))]), 'zugdetails')
            if stsCon.read_xml_single(traindetailsxml, 'zugdetails', 'sichtbar') == 'true':
                j.visible = True
                self.trains.add(j)
                self.trainsInvisible.remove(j)
            
            
