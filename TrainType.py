import logging

logger = logging.getLogger(__name__)

class TrainType:
    def __init__(self, name, country):
        self.traintype = ''
        self.prefix = ''
        self.freight = ()
        self.longdistance = ()
        self.regional = ()
        self.city = ()
        self.special = ()
        self.loco = ()
        self.construction = ()
        self.other = ()
        self.determineTrainType(name, country)
        
    def determineTrainType(self, name, country):
        match country:
            case 'BE':
                self.freight = ('G', 'TFI', 'CT')
                self.longdistance = ('TVG', 'IC')
                self.regional = ('P', 'L')
                self.city = ('S')
                self.special = ('M')
                self.loco = ('LT', 'LR', 'SCHADW', 'Lok', 'RF', 'RA')
                self.construction = ('BAUZ', 'TFZF')
                self.prefix = name[0:name.index(' ')]# substring(0, name.substring(0, index(' ')))
            case 'DK'|'FR'|'GB'|'LU'|'NL'|'AT'|'CH'|'PL'|'CZ':
                logger.warning('Country ' + country + ' currently not defined!')
            case 'IT':
                self.freight = ('MRS', 'TCS', 'EUC', 'TEC', 'TC', 'MRV', 'MRI', 'MI', 'MT', 'TME')
                self.longdistance = ('EXP', 'EC', 'IC', 'EN', 'ES', 'AV', 'TGV')
                self.regional = ('REG', 'MET', 'RE', 'RV', 'R', 'MXP')
                self.city = ('Sx'. 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'SFM')
                self.special = ('CP', 'STM')
                self.loco = ('TRA', 'INV', 'LIS', 'm')
                self.construction = ('NCL')
                self.prefix = name[0:name.index(' ')]
            case 'SE':
                self.freight = ('G', 'Gt')
                self.longdistance = ('X', 'SJ', 'MTR', 'Natt', 'MTR', 'Snäll', 'FLX', 'Saga', 'Tågab')
                self.regional = ('SJ', 'Mälab', 'TiB', 'ØP', 'ØK')
                self.city = ('SL', 'AEX', 'Påga', 'UL')
                self.special = ('M')
                self.loco = ('Lok', 'V')
                self.construction = ('Tjt')
                self.prefix = name[0:name.index(' ')]
            case 'DE':
                self.freight = ('CB', 'CbZ', 'CFA', 'CFN', 'CHL', 'CIL', 'CL', 'CS', 'CSQ', 'CT', 'DFG', 'DGE', 'DGN', 'DGS', 'DGX', 'DGZ', 'DNG', 'EnKo', 'EUC', 'ExC', 'EZ', 'EZK', 'FE', 'FIR', 'FR', 'FS', 'FX', 'FZ', 'FZT', 'GAG', 'GAGC', 'GC', 'GX', 'GZ', 'HGK', 'ICG', 'ICL', 'IKE', 'IKL', 'IKS', 'IRC', 'KC', 'KCL', 'KT', 'NG', 'PIC', 'RA', 'RWE', 'TC', 'TEC', 'Tfzl', 'TKC', 'TRC')
                self.longdistance = ('AS', 'AZ', 'CNL', 'D', 'DLr', 'DLt', 'DPE', 'DPF', 'EC', 'EN', 'FLX', 'IC', 'ICE', 'LNF', 'LPF', 'LPFT', 'LR', 'LRV', 'LRZ', 'NJ', 'RJ', 'RJX', 'TGV', 'THA', 'VX', 'WEST', 'X')
                self.regional = ('ABR', 'AKN', 'ALX', 'BOB', 'CAN', 'DNR', 'EIB', 'ERB', 'EVB', 'FEG', 'FEX', 'HEX', 'HLB', 'HTB', 'HZL', 'IRE', 'LT', 'ME', 'MEr', 'MR', 'MRB', 'NBE', 'NEB', 'NEG', 'NOB', 'NWB', 'OE', 'OLA', 'PEG', 'PRE', 'RB', 'RbZ', 'RE', 'RTB', 'SBB', 'SHB', 'STB', 'SWE', 'UBB', 'VBG', 'VEC', 'VIA', 'WEG', 'WFB', 'BRB', 'RB-D', 'RE-D', 'DPN', 'DPN-G')
                self.city = ('BSB', 'CBC', 'Dsts', 'B', 'G', 'H', 'I', 'P', 'W', 'E', 'LS', 'OSB', 'RT', 'S', 'Messeshuttle', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9')
                self.special = ('DbZ', 'DZ', 'M', 'MCT', 'PbZ', 'SDZ')
                self.loco = ('L', 'Lok', 'LOK', 'LOKF', 'LZ', 'Rf', 'Schadl', 'C', 'F', 'R', 'Schadt', 'Schadw', 'T', 'Tfzf', 'Ersatzlok')
                self.construction = ('Bauz', 'DGV')
                try:
                    self.prefix = name[0:name.index(' ')]
                except:
                    # case without number, i.e. Messeshuttle in Augsburg
                    self.prefix = name
            case _:
                logger.warning('Country ' + country + ' not known. No categories available!')
                self.prefix = ''
                self.traintype = 'OTHER'
            
        if self.prefix in self.freight:
            self.traintype = 'FREIGHT'
        elif self.prefix in self.longdistance:
            self.traintype = 'LONGDISTANCE'
        elif self.prefix in self.regional:
            self.traintype = 'REGIONAL'
        elif self.prefix in self.city:
            self.traintype = 'CITY'
        elif self.prefix in self.special:
            self.traintype = 'SPECIAL'
        elif self.prefix in self.loco:
            self.traintype = 'LOCO'
        elif self.prefix in self.construction:
            self.traintype = 'CONSTRUCTION'
        else:
            self.traintype = 'OTHER'
