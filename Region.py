import logging
logger = logging.getLogger(__name__)

class Region:
    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.country = self.getCountry()
        logger.debug('region is: ' + self.region + ' in ' + self.country)

    def getCountry(self):
        if self.region == 'Belgien':
            return 'BE'
        elif self.region.startswith('Danmark'):
            return 'DK'
        elif self.region == 'Grand Est' or 'France' in self.region:
            return 'FR'
        elif self.region.startswith('Großbrittanien'):
            return 'GB'
        elif 'Italien' in self.region:
            return 'IT'
        elif self.region == 'Luxemburg':
            return 'LU'
        elif self.region.startswith('Niederlande'):
            return 'NL'
        elif self.region.startswith('Österreich'):
            return 'AT'
        elif 'schweiz' in self.region or self.region.startswith('Tessin') or self.region.startswith('Zürich'):
            return 'CH'
        elif self.region == 'Polen':
            return 'PL'
        elif self.region == 'Sverige':
            return 'SE'
        elif self.region.startswith('Tschechien'):
            return 'CZ'
        else:
            return 'DE'
