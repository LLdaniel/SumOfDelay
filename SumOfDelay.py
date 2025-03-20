from StsConnector import StsConnector
from Statistics import Statistics
from nicegui import ui
from Ui import Ui
import logging
import argparse

##################################################################
host = '127.0.0.1'  # Replace with the server IP or hostname
port = 3691         # Replace with the desired port
version = '0.0.1'   # Plugin version
interval = 30.0     # update interval [s]
##################################################################

# parsing
parser = argparse.ArgumentParser()
parser.add_argument( '-l',
                     '--loglevel',
                     default='warning',
                     help='Provide logging level like error, warning, info, debug, default=warning' )
args = parser.parse_args()

# logging
logger = logging.getLogger()
logger.setLevel(args.loglevel.upper())

stream_handler = logging.StreamHandler()
stream_handler.setLevel(args.loglevel.upper())
formatter = logging.Formatter('[%(asctime)s ::%(levelname)s:: %(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
############################################################

def worker(sodUi, stats, stsCon):
    logger.debug('------Now updating...------')
    stats.update(stsCon)
    sodUi.update(stats.delay)
    logger.debug(repr(stats.trains))
    logger.debug(repr(stats.trainsInvisible))
    logger.debug(stats.delay)
    logger.debug('------... update done!------')

##########################################################
# Create a new connection to Stellwerksim
stsCon = StsConnector(host, port)
stsCon.register(version)
stats = Statistics()

# initially set train lists
for t in stsCon.trainlist:
    stats.add_train(t)

# UI part
sodUi = Ui(stsCon.region.name)
ui.timer(interval, lambda: worker(sodUi, stats, stsCon))
ui.run(title='Sum Of Delay', favicon='🚆', reload=True)
